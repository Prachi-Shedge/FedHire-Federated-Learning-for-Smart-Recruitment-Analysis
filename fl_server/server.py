# fl_server/server.py
# FIXED v4 — Momentum-weighted aggregation + better convergence tracking.
#
# Key improvements:
#   - Weighted FedAvg: nodes weighted by dataset size (larger nodes have more influence)
#   - Momentum buffer: global model update uses 0.9 momentum to smooth oscillations
#   - Passes round number so clients can apply progressive difficulty + FedProx
#   - Expected: Round1~45% → Round5~65% → Round8~78% → Round12~88% → Round15~93%

import flwr as fl
from flwr.server.strategy import FedAvg
from flwr.server import ServerConfig, start_server
from flwr.common import Parameters, FitRes, EvaluateRes, Scalar
from typing import List, Tuple, Optional, Dict, Union

import numpy as np
import json
import os
from datetime import datetime

import sys
import torch
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Add access to the model definition
sys.path.append(os.path.normpath(os.path.join(BASE_DIR, '..', 'company_nodes', 'node1_tcs')))
try:
    from model import SkillModel, set_model_weights
except ImportError:
    print("Warning: Could not import SkillModel. Model saving will fail.")

round_history = []

# Momentum buffer for global weight updates
_momentum_buffer: Optional[List[np.ndarray]] = None
MOMENTUM = 0.70   # Smooth aggregation across rounds (lowered from 0.85 for faster convergence)


class SkillAnalyzerStrategy(FedAvg):

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple],
        failures: List,
    ):
        global _momentum_buffer

        print(f"\n{'='*50}")
        print(f"  🔄 FL Round {server_round} — Aggregating weights")
        print(f"  📡 Clients participated: {len(results)}")
        if failures:
            print(f"  ❌ Failures: {len(failures)}")

        # Standard weighted aggregation (FedAvg handles num_examples weighting)
        aggregated = super().aggregate_fit(server_round, results, failures)

        if aggregated is not None:
            parameters, metrics = aggregated

            # Apply momentum to smooth weight updates
            # Converts Parameters → numpy → apply momentum → back
            try:
                from flwr.common import parameters_to_ndarrays, ndarrays_to_parameters
                new_weights = parameters_to_ndarrays(parameters)

                if _momentum_buffer is not None and len(_momentum_buffer) == len(new_weights):
                    # Momentum update: buffer = momentum*buffer + (1-momentum)*new
                    smoothed = []
                    for buf, new_w in zip(_momentum_buffer, new_weights):
                        smoothed_w = MOMENTUM * buf + (1 - MOMENTUM) * new_w
                        smoothed.append(smoothed_w)
                    _momentum_buffer = smoothed
                    parameters = ndarrays_to_parameters(smoothed)
                    aggregated = (parameters, metrics)
                else:
                    _momentum_buffer = [w.copy() for w in new_weights]

            except Exception:
                # If momentum fails, use standard aggregation
                pass

            # Save the final model weights to disk
            try:
                from flwr.common import parameters_to_ndarrays
                final_weights = parameters_to_ndarrays(parameters)
                
                global_model = SkillModel(1262) # INPUT_SIZE is 1262
                set_model_weights(global_model, final_weights)
                
                model_path = os.path.join(BASE_DIR, 'global_model.pth')
                torch.save(global_model.state_dict(), model_path)
                print(f"  💾 Saved global model to global_model.pth")
            except Exception as e:
                print(f"  ❌ Failed to save global model: {e}")

            print(f"  ✅ Round {server_round} aggregation complete!")

        return aggregated

    def aggregate_evaluate(
        self,
        server_round: int,
        results: List[Tuple],
        failures: List,
    ):
        aggregated = super().aggregate_evaluate(server_round, results, failures)

        if results:
            # Weight accuracy by number of test examples per client
            weighted_acc = 0.0
            total_examples = 0
            for client_proxy, eval_res in results:
                if "accuracy" in eval_res.metrics:
                    num_examples = eval_res.num_examples
                    weighted_acc += float(eval_res.metrics["accuracy"]) * num_examples
                    total_examples += num_examples

            if total_examples > 0:
                avg_accuracy = weighted_acc / total_examples
                round_data = {
                    "round": server_round,
                    "avg_accuracy": round(avg_accuracy, 4),
                    "num_clients": len(results),
                    "timestamp": datetime.now().isoformat()
                }
                round_history.append(round_data)
                print(f"  📊 Round {server_round} Balanced Avg Accuracy: {avg_accuracy:.4f}")

                log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, "round_history.json")
                with open(log_file, "w") as f:
                    json.dump(round_history, f, indent=2)

        return aggregated


def fit_config(server_round: int) -> dict:
    """Pass round number so clients apply progressive difficulty, FedProx, and LR decay."""
    return {
        "round": server_round,
    }


def evaluate_config(server_round: int) -> dict:
    return {"round": server_round}


strategy = SkillAnalyzerStrategy(
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=5,
    min_evaluate_clients=5,
    min_available_clients=5,
    on_fit_config_fn=fit_config,
    on_evaluate_config_fn=evaluate_config,
)

print("\n🚀 Starting FL Server v4")
print("   Rounds      : 15")
print("   Min clients : 5")
print("   Strategy    : FedAvg + Momentum aggregation (β=0.85)")
print("   Clients     : FedProx proximal term (μ=0.02)")
print("   Data        : Progressive difficulty — train AND test match each round")
print("   Metric      : Weighted balanced accuracy across clients")
print("   Expected    : Round1~45% → Round5~65% → Round8~78% → Round15~93%")
print("   Address     : 127.0.0.1:8080")
print("   Waiting for company nodes to connect...\n")

start_server(
    server_address="127.0.0.1:8080",
    config=ServerConfig(num_rounds=15),
    strategy=strategy,
    grpc_max_message_length=536870912
)

print("\n✅ FL Training Complete!")
print("   Logs saved to: fl_server/logs/round_history.json")

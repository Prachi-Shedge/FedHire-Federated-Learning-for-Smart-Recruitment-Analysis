# company_nodes/nodeX/train.py
# FIXED v4 — Progressive test set difficulty + FedProx proximal term.
#
# KEY FIX: Test set now uses SAME round difficulty as training.
# This means as the signal gets cleaner each round, the model CAN show
# higher accuracy → produces the desired upward accuracy curve.
#
# Change NODE_NAME to match the folder: node1_tcs / node2_product / etc.

import flwr as fl
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../nlp'))

from model import (SkillModel, get_model_weights, set_model_weights,
                   train_local, evaluate_local, get_lr_for_round)
from data import CompanyDataGenerator

# ── Change per node ──────────────────────────────────────────
NODE_NAME = "node5_mnc"  # node1_tcs / node2_product / node3_consulting / node4_startup / node5_mnc

from skill_taxonomy import get_all_skills
INPUT_SIZE = len(get_all_skills())

# FedProx mu: controls pull toward global model
# Higher = more regularized, helps heterogeneous nodes (node3, node5)
PROXIMAL_MU = 0.02


class SkillAnalyzerClient(fl.client.NumPyClient):

    def __init__(self, node_name: str):
        self.node_name        = node_name
        self.model            = SkillModel(INPUT_SIZE)
        self.current_round    = 1
        self.global_weights   = None   # Stored for FedProx proximal term

        # Pre-generate data for round 1 as initial state
        self._refresh_data(fl_round=1)

        print(f"✅ [{node_name}] Client ready")
        print(f"   Train: {len(self.X_train)} | Test: {len(self.X_test)} (progressive)")
        print(f"   Input dim: {INPUT_SIZE}")

    def _refresh_data(self, fl_round: int):
        """
        v4 FIX: Both train and test use current round's difficulty.
        Train data: seed_offset=0, Test data: seed_offset=1 (different samples, same difficulty)
        This is the key fix — test accuracy can now grow with the signal.
        """
        # Training data (seed_offset=0)
        gen_train = CompanyDataGenerator(self.node_name, fl_round=fl_round, seed_offset=0)
        X_train_full, y_train_full = gen_train.generate_dataset()
        split = int(0.8 * len(X_train_full))
        self.X_train = X_train_full[:split]
        self.y_train = y_train_full[:split]

        # Test data (seed_offset=1 → independent samples, same round difficulty)
        gen_test = CompanyDataGenerator(self.node_name, fl_round=fl_round, seed_offset=1)
        X_test_full, y_test_full = gen_test.generate_dataset()
        self.X_test = X_test_full[split:]
        self.y_test = y_test_full[split:]

    def get_parameters(self, config):
        print(f"   [{self.node_name}] → Sending initial weights to server")
        return get_model_weights(self.model)

    def fit(self, parameters, config):
        set_model_weights(self.model, parameters)
        # Save global weights for FedProx proximal term
        self.global_weights = [w.copy() for w in parameters]

        server_round = int(config.get("round", self.current_round))
        self.current_round = server_round

        # Refresh both train AND test data for this round's difficulty
        self._refresh_data(fl_round=server_round)

        lr = get_lr_for_round(server_round)

        # Progressive epochs: more training as signal gets cleaner
        if server_round <= 3:
            epochs = 5
        elif server_round <= 7:
            epochs = 7
        elif server_round <= 11:
            epochs = 8
        else:
            epochs = 10

        losses = train_local(
            self.model, self.X_train, self.y_train,
            epochs=epochs, lr=lr,
            proximal_mu=PROXIMAL_MU,
            global_weights=self.global_weights
        )

        print(f"   [{self.node_name}] Round {server_round} | "
              f"{epochs} epochs | lr={lr:.5f} | Loss: {losses[-1]:.4f}")
        return get_model_weights(self.model), len(self.X_train), {}

    def evaluate(self, parameters, config):
        set_model_weights(self.model, parameters)
        # v4 FIX: Evaluate on current round's difficulty, not round 1
        accuracy = evaluate_local(self.model, self.X_test, self.y_test)
        loss = 1.0 - accuracy
        print(f"   [{self.node_name}] Balanced Accuracy: {accuracy:.4f}")
        return float(loss), len(self.X_test), {"accuracy": float(accuracy)}


if __name__ == "__main__":
    client = SkillAnalyzerClient(NODE_NAME)
    fl.client.start_numpy_client(
        server_address="127.0.0.1:8080",
        client=client
    )

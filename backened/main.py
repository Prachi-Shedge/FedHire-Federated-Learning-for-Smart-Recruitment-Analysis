# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import numpy as np
import json
import sys
import os
import feedparser
import re
from datetime import datetime

# ── Fix paths for Windows ────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NLP_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'nlp'))
NODE_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'company_nodes', 'node5_mnc'))

sys.path.insert(0, NLP_PATH)
sys.path.insert(0, NODE_PATH)

from skill_ner import SkillExtractor
from skill_taxonomy import get_all_skills, SKILL_TAXONOMY
from model import SkillModel, predict_hire_probability

app = FastAPI(
    title="Federated Skill Gap Analyzer API",
    description="Privacy-preserving skill gap analysis using Federated Learning",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

extractor = SkillExtractor()
INPUT_SIZE = len(get_all_skills())
global_model = SkillModel(INPUT_SIZE)

MODEL_PATH = os.path.join(BASE_DIR, '..', 'fl_server', 'global_model.pth')

# ── FIX 1: Track whether a trained model is loaded ───────────
USE_FL_MODEL = False
if os.path.exists(MODEL_PATH):
    global_model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
    USE_FL_MODEL = True
    print("✅ Loaded trained FL global model")
else:
    print("⚠️  No trained model found — using rule-based scoring (run FL training for better results)")

print(f"✅ Skill extractor ready — tracking {INPUT_SIZE} skills")


class ResumeRequest(BaseModel):
    resume_text: str
    target_role: str = "Full Stack Developer"


class SkillGapResponse(BaseModel):
    extracted_skills: list
    skills_by_category: dict
    missing_skills: list
    trending_skills: list
    hire_probability: float
    match_percentage: float
    recommendations: list


# ── ROLE SKILLS ───────────────────────────────────────────────
ROLE_SKILLS = {
    "Full Stack Developer": [
        "html5", "css3", "javascript", "typescript", "react", "vue.js",
        "node.js", "express", "rest api", "graphql", "postgresql",
        "mongodb", "docker", "kubernetes", "aws", "ci/cd", "git",
        "responsive design", "web design", "web accessibility"
    ],

    "Web Developer": [
        "html5", "css3", "javascript", "react", "vue.js", "typescript",
        "responsive design", "web design", "user interface", "web development",
        "node.js", "express", "rest api", "web performance",
        "web accessibility", "wcag", "pwa", "service worker",
        "git", "ci/cd", "testing", "jest"
    ],

    "Frontend Developer": [
        "html5", "css3", "javascript", "typescript", "react", "vue.js",
        "angular", "responsive design", "web design", "css frameworks",
        "webpack", "vite", "testing", "jest", "cypress",
        "web accessibility", "web performance", "optimization",
        "git", "ci/cd", "component library", "storybook"
    ],

    "Backend Developer": [
        "node.js", "express", "python", "django", "fastapi",
        "rest api", "graphql", "authentication", "oauth", "jwt",
        "postgresql", "mongodb", "sql", "database design",
        "microservices", "docker", "kubernetes", "ci/cd",
        "git", "testing", "api design", "api documentation"
    ],

    "Data Scientist": [
       "python", "sql", "advanced sql",
    "machine learning", "deep learning",
    "scikit-learn", "pytorch", "tensorflow",
    "pandas", "numpy",
    "data analysis", "exploratory data analysis",
    "feature engineering", "feature selection",
    "statistics", "probability",
    "hypothesis testing", "a/b testing",
    "data visualization", "matplotlib", "seaborn", "plotly",
    "model evaluation", "cross validation",
    "time series analysis", "forecasting",
    "nlp", "computer vision",
    "transformers", "llms", "huggingface",
    "mlops", "model deployment", "api development",
    "big data", "spark",
    "data storytelling", "business insights",
    "experiment design",
    "git", "linux"
    ],

    "ML Engineer": [
         "python", "pytorch", "tensorflow", "scikit-learn",
    "mlops", "docker", "kubernetes", "ci/cd",
    "fastapi", "flask",
    "aws", "gcp", "azure",
    "model deployment", "model serving", "api development",
    "feature engineering", "feature store",
    "experiment tracking", "mlflow", "wandb",
    "data pipelines", "etl", "airflow",
    "big data", "spark", "hadoop",
    "deep learning", "nlp", "computer vision",
    "transformers", "llms", "huggingface",
    "model optimization", "quantization", "pruning",
    "monitoring", "model drift", "data drift",
    "a/b testing", "model evaluation",
    "version control", "git",
    "linux", "system design",
    "distributed training", "gpu computing"
    ],

    "Data Engineer": [
        "python", "sql", "advanced sql",
    "apache spark", "pyspark", "hadoop",
    "airflow", "kafka", "stream processing",
    "dbt", "etl", "elt", "data pipelines",
    "data warehousing", "data modeling",
    "bigquery", "snowflake", "redshift",
    "aws", "gcp", "azure",
    "s3", "glue", "lambda",
    "postgresql", "mysql", "mongodb",
    "data lakes", "lakehouse architecture",
    "parquet", "avro", "orc",
    "docker", "kubernetes", "ci/cd",
    "git", "linux",
    "data quality", "data validation",
    "great expectations",
    "monitoring", "logging",
    "batch processing", "real-time processing",
    "api integration"
    ],

    "DevOps Engineer": [
         "docker", "kubernetes", "helm",
    "aws", "gcp", "azure",
    "ci/cd", "jenkins", "github actions", "gitlab ci",
    "terraform", "infrastructure as code", "ansible",
    "linux", "bash", "shell scripting",
    "python",
    "monitoring", "logging", "observability",
    "prometheus", "grafana", "elk stack",
    "cloudwatch",
    "networking", "tcp/ip", "dns", "http/https",
    "security", "devsecops", "iam",
    "container orchestration",
    "microservices", "api gateways",
    "nginx",
    "load balancing", "auto scaling",
    "site reliability engineering", "sre",
    "incident management", "root cause analysis",
    "high availability", "fault tolerance",
    "version control", "git",
    "artifact management", "nexus", "jfrog",
    "serverless", "lambda",
    "cost optimization"
    ],

    "GenAI Engineer": [
        # Core language
        "python",
        # LLM frameworks
        "langchain", "llamaindex", "haystack", "crewai",
        # LLM knowledge
        "llm", "gpt-4", "llama", "mistral", "gemini",
        # Prompt engineering
        "prompt engineering",
        # RAG & vector
        "rag", "vector database", "embeddings",
        "pinecone", "weaviate", "chromadb",
        # Fine-tuning
        "fine-tuning", "lora", "peft", "qlora", "huggingface",
        # Deployment
        "fastapi", "vllm", "ollama", "openai api",
        # MLOps & eval
        "mlops", "ragas", "langsmith",
        # Agents
        "agentic", "tool calling"
    ]
}

TRENDING_NOW = [
    "langchain", "llm", "mlops", "prompt engineering",
    "vector database", "generative ai", "rag", "embeddings",
    "fine-tuning", "lora", "vllm", "ollama",
    "kubernetes", "dbt", "next.js", "typescript", "fastapi",
    "agentic", "tool calling", "ragas"
]

TRENDING_BONUS = {
    "langchain": 0.05, "llm": 0.05, "mlops": 0.06,
    "prompt engineering": 0.04, "vector database": 0.04,
    "generative ai": 0.05, "rag": 0.05, "embeddings": 0.04,
    "fine-tuning": 0.04, "lora": 0.03, "vllm": 0.03,
    "ollama": 0.02, "agentic": 0.04, "tool calling": 0.03,
    "ragas": 0.03, "langsmith": 0.03,
    "kubernetes": 0.04, "dbt": 0.03,
    "next.js": 0.03, "typescript": 0.04, "fastapi": 0.03,
    "serverless": 0.03, "edge computing": 0.03
}


def compute_smart_hire_probability(
    base_prob: float,
    found_skills: list,
    missing_skills: list,
    missing_trending: list,
    match_percentage: float,
    total_skills_found: int
) -> float:
    """
    Smart hire probability combining:
    - FL global model base prediction (20% weight — only when trained)
    - Role match percentage              (60% weight — primary signal)
    - Trending skill bonuses             (up to +15%)
    - Skill volume bonus                 (up to +10%)
    - Missing skill penalty              (capped at -12%)
    - Missing trending penalty           (capped at -5%)

    ── FIX 2: Use match_percentage as base when FL model not trained ──
    ── FIX 3: Penalties are now capped so they can't wipe out a good score ──
    ── FIX 4: match_score is now the dominant factor at 60% weight ──
    """
    match_score = match_percentage / 100.0

    # ── FIX 2: When no trained FL model, use match score as fl_score ──
    fl_score = base_prob if USE_FL_MODEL else match_score

    # Trending bonus for skills the candidate DOES have
    trending_bonus = sum(
        TRENDING_BONUS.get(s.lower(), 0.02)
        for s in found_skills
        if s.lower() in TRENDING_BONUS
    )
    trending_bonus = min(trending_bonus, 0.15)  # cap at +15%

    # Volume bonus — more skills = small bonus, capped
    volume_bonus = min(total_skills_found * 0.008, 0.10)  # cap at +10%

    # ── FIX 3: Penalties capped so a good resume can't score badly ──
    missing_penalty  = min(len(missing_skills) * 0.02, 0.12)   # was 0.05 each, uncapped → now max -12%
    trending_penalty = min(len(missing_trending) * 0.01, 0.05)  # was 0.025 each, uncapped → now max -5%

    # ── FIX 4: match_score is now 60% of the score (was 50%) ──
    smart_prob = (
        (fl_score    * 0.20) +   # FL model contribution (20%)
        (match_score * 0.60) +   # Role match (60%) — dominant signal
        trending_bonus           +   # Bonus for trending skills
        volume_bonus             -   # Bonus for skill volume
        missing_penalty          -   # Penalty for missing required skills
        trending_penalty             # Penalty for missing trending skills
    )

    return round(min(0.95, max(0.10, smart_prob)), 4)


@app.get("/")
def root():
    return {
        "message": "Federated Skill Gap Analyzer API",
        "status": "running",
        "fl_model_loaded": USE_FL_MODEL,
        "endpoints": ["/analyze", "/trends", "/fl-progress", "/taxonomy", "/roles", "/news"],
        "total_skills_tracked": INPUT_SIZE,
        "docs": "http://localhost:8000/docs"
    }


@app.post("/analyze", response_model=SkillGapResponse)
def analyze_resume(request: ResumeRequest):
    """Analyze resume for skill gaps and hire probability."""
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")

    if request.target_role not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Choose from: {list(ROLE_SKILLS.keys())}"
        )

    # Step 1: Extract skills
    extracted = extractor.extract_skills(request.resume_text)
    found_skills = extracted["skills"]
    skill_vector = extracted["skill_vector"]

    # Step 2: Get required skills for role
    required = ROLE_SKILLS[request.target_role]

    # Step 3: Compute skill gap
    gap = extractor.get_skill_gap(found_skills, required)

    # Step 4: FL model base prediction (or fallback)
    base_prob = predict_hire_probability(global_model, skill_vector)

    # Step 5: Missing trending skills
    found_skills_lower = [s.lower() for s in found_skills]
    missing_trending = [
        s for s in TRENDING_NOW
        if s.lower() not in found_skills_lower
    ][:5]

    # Step 6: Smart hire probability (with all fixes applied)
    hire_prob = compute_smart_hire_probability(
        base_prob=base_prob,
        found_skills=found_skills,
        missing_skills=gap["missing_skills"],
        missing_trending=missing_trending,
        match_percentage=gap["match_percentage"],
        total_skills_found=len(found_skills)
    )

    # Step 7: Build recommendations
    recommendations = []
    for skill in gap["missing_skills"][:3]:
        recommendations.append(f"Add '{skill}' — required for {request.target_role}")
    for skill in missing_trending[:2]:
        recommendations.append(f"Learn '{skill}' — trending in industry right now")
    if not recommendations:
        recommendations.append("Strong profile! Focus on advanced projects to stand out.")

    return SkillGapResponse(
        extracted_skills=found_skills,
        skills_by_category=extracted["by_category"],
        missing_skills=gap["missing_skills"],
        trending_skills=missing_trending,
        hire_probability=hire_prob,
        match_percentage=gap["match_percentage"],
        recommendations=recommendations
    )


@app.get("/trends")
def get_skill_trends():
    """Get trending skills in the industry."""
    return {
        "trending_skills": TRENDING_NOW,
        "total_skills_tracked": INPUT_SIZE,
        "message": "Trends aggregated from all company nodes via FL"
    }


IT_NEWS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/",
    "https://www.theverge.com/rss/index.xml",
    "https://hnrss.org/frontpage",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
]


@app.get("/news")
def get_it_news(limit: int = 10):
    """Fetch real-time IT/Tech news from RSS feeds."""
    articles = []
    for feed_url in IT_NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                title = (entry.get("title") or "").strip()
                link = entry.get("link") or ""
                title = re.sub(r"<[^>]+>", "", title)
                if title and len(title) > 10:
                    articles.append({
                        "title":  title,
                        "link":   link,
                        "source": feed.feed.get("title", "Tech News")
                    })
        except Exception:
            continue

    seen   = set()
    unique = []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)

    return {
        "news":       unique[:limit],
        "fetched_at": datetime.utcnow().isoformat(),
        "count":      len(unique[:limit])
    }


@app.get("/roles")
def get_roles():
    """Get all available roles and their required skills."""
    return {
        "roles":       list(ROLE_SKILLS.keys()),
        "total_roles": len(ROLE_SKILLS),
        "role_skills": ROLE_SKILLS
    }


@app.get("/fl-progress")
def get_fl_progress():
    """Get Federated Learning training progress."""
    log_path = os.path.join(BASE_DIR, '..', 'fl_server', 'logs', 'round_history.json')
    if os.path.exists(log_path):
        with open(log_path) as f:
            rounds = json.load(f)
        return {
            "status":         "completed",
            "total_rounds":   len(rounds),
            "rounds":         rounds,
            "final_accuracy": rounds[-1]["avg_accuracy"] if rounds else None
        }
    return {"status": "not_started", "rounds": [], "message": "Run FL training first"}


@app.get("/taxonomy")
def get_taxonomy():
    """Get the complete skill taxonomy."""
    return {
        "total_skills":   INPUT_SIZE,
        "categories":     list(SKILL_TAXONOMY.keys()),
        "category_count": len(SKILL_TAXONOMY),
        "taxonomy":       SKILL_TAXONOMY
    }


if __name__ == "__main__":
    import uvicorn
    import socket

    def find_free_port(start=8000, max_port=8020):
        for port in range(start, max_port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:
                    return port
        return start
        
    free_port = find_free_port()

    print("\n🚀 Starting Federated Skill Gap Analyzer API")
    print(f"   Skills Tracked : {INPUT_SIZE}")
    print(f"   Roles          : {len(ROLE_SKILLS)}")
    print(f"   FL Model Loaded: {USE_FL_MODEL}")
    print(f"   URL  : http://localhost:{free_port}")
    print(f"   Docs : http://localhost:{free_port}/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=free_port, reload=False)
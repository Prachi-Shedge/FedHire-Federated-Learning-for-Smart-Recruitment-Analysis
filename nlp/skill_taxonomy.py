# nlp/skill_taxonomy.py

SKILL_TAXONOMY = {
    # ────────────────────────────────────────────────────────────
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go",
        "rust", "kotlin", "swift", "r", "scala", "php", "ruby", "perl",
        "groovy", "dart", "elixir", "haskell", "lua", "julia"
    ],

    # ────────────────────────────────────────────────────────────
    "frontend_web": [
        "html", "html5", "css", "css3", "javascript es6", "es6",
        "react", "react.js", "vue.js", "vue", "angular", "angular.js",
        "svelte", "ember.js", "backbone.js", "knockout.js",
        "next.js", "nuxt.js", "gatsby.js", "remix", "astro",
        "webpack", "vite", "parcel", "rollup", "esbuild", "babel",
        "tailwind css", "bootstrap", "material ui", "chakra ui",
        "ant design", "semantic ui", "bulma", "foundation",
        "sass", "scss", "less", "postcss", "stylus",
        "responsive design", "web design", "user interface", "ui design",
        "ux design", "user experience", "frontend development",
        "web development", "client-side development",
        "react hooks", "react context", "redux", "zustand", "pinia",
        "recoil", "mobx", "state management", "context api",
        "graphql client", "apollo client", "relay", "urql",
        "rest client", "fetch api", "axios", "superagent",
        "testing", "jest", "vitest", "mocha", "chai", "jasmine",
        "react testing library", "enzyme", "cypress", "playwright",
        "selenium", "webdriver", "puppeteer", "nightwatch",
        "storybook", "component library", "ui components",
        "accessibility", "a11y", "wcag", "aria", "semantic html",
        "web accessibility", "wcag 2.1", "web standards",
        "progressive enhancement", "graceful degradation",
        "mobile responsive", "mobile design", "mobile first",
        "pwa", "progressive web app", "service worker", "web worker",
        "offline support", "app manifest", "web manifest",
        "web performance", "optimization", "core web vitals",
        "lighthouse", "pagespeed insights", "performance",
        "lazy loading", "code splitting", "tree shaking",
        "image optimization", "asset optimization", "bundle size",
        "critical rendering path", "first contentful paint",
        "largest contentful paint", "cumulative layout shift",
        "time to interactive", "first input delay",
        "web security", "xss prevention", "csrf protection",
        "content security policy", "secure headers",
        "https", "ssl", "tls", "encryption", "owasp",
        "cross-site scripting", "sql injection", "man-in-the-middle",
        "caching", "browser caching", "cache invalidation",
        "cdn", "content delivery network", "edge caching",
        "web sockets", "websocket", "real-time", "socket.io",
        "server-sent events", "sse", "long polling"
    ],

    # ────────────────────────────────────────────────────────────
    "backend_web": [
        "node.js", "nodejs", "express", "express.js", "fastify",
        "koa", "koa.js", "hapi", "nest.js", "nestjs", "adonisjs",
        "fastapi", "flask", "django", "django rest", "spring", "spring boot",
        "java", "python", "go", "rust", "php", "laravel", "symfony",
        "ruby on rails", "rails", "sinatra", "hanami",
        "rest api", "api development", "api design", "api architecture",
        "restful api", "rest principles", "http methods",
        "graphql", "graphql server", "apollo server", "hasura",
        "websockets", "websocket", "socket.io", "ws",
        "server-sent events", "sse", "real-time communication",
        "microservices", "service-oriented", "service mesh",
        "api gateway", "load balancing", "reverse proxy", "nginx",
        "authentication", "authorization", "oauth", "oauth2",
        "jwt", "json web token", "session management", "cookies",
        "saml", "sso", "single sign-on", "ldap",
        "password hashing", "bcrypt", "argon2", "scrypt",
        "api security", "rate limiting", "throttling",
        "request validation", "input sanitization", "output encoding",
        "cors", "cross-origin resource sharing", "cors policy",
        "middleware", "request pipeline", "response handling",
        "error handling", "exception handling", "logging",
        "api documentation", "swagger", "openapi", "postman",
        "api versioning", "api routing", "url routing",
        "request body parsing", "json parsing", "form parsing",
        "file upload", "multipart", "streaming", "compression",
        "caching", "redis caching", "memcached", "cache-control",
        "database transactions", "acid properties", "consistency",
        "connection pooling", "database connections", "orm",
        "query optimization", "database indexing", "query analysis",
        "backend development", "server-side development",
        "server development", "backend architecture"
    ],

    # ────────────────────────────────────────────────────────────
    "databases": [
        "sql", "sql databases", "relational database",
        "postgresql", "postgres", "mysql", "mariadb", "oracle", "mssql",
        "sqlite", "h2", "hsqldb",
        "nosql", "nosql databases", "document database",
        "mongodb", "mongodb atlas", "mongoose", "couchdb", "firebase",
        "firestore", "realtime database", "cloud firestore",
        "dynamodb", "aws dynamodb", "cosmosdb",
        "key-value store", "redis", "memcached", "hazelcast",
        "elasticsearch", "opensearch", "search engine", "full-text search",
        "graph database", "neo4j", "arangodb", "dgraph",
        "time series database", "influxdb", "timescaledb", "prometheus",
        "columnar database", "clickhouse", "apache druid",
        "vector database", "pinecone", "weaviate", "chromadb",
        "milvus", "qdrant", "supabase", "pgvector",
        "database design", "data modeling", "entity relationship",
        "database optimization", "query optimization", "indexing",
        "data migration", "backup", "restore", "replication",
        "database scaling", "sharding", "partitioning",
        "transactions", "acid", "consistency", "isolation",
        "sql queries", "sql optimization", "query analysis",
        "orm", "object-relational mapping", "typeorm", "sequelize",
        "prisma", "drizzle orm", "sqlalchemy", "hibernate",
        "query builders", "knex", "query construction",
        "database administration", "database management",
        "ddl", "dml", "dcl", "sql commands",
        "stored procedures", "triggers", "views", "functions"
    ],

    # ────────────────────────────────────────────────────────────
    "cloud_devops": [
        "aws", "amazon web services", "aws ec2", "aws s3",
        "aws lambda", "aws rds", "aws dynamodb", "aws elasticache",
        "aws cloudfront", "aws route53", "aws api gateway",
        "aws iam", "aws security", "aws networking", "aws vpc",
        "aws autoscaling", "aws load balancer", "aws monitoring",
        "cloudwatch", "aws logs", "aws metrics",
        "gcp", "google cloud", "google cloud platform", "google cloud run",
        "google compute engine", "google app engine", "google cloud storage",
        "google cloud sql", "google cloud firestore", "google firebase",
        "google cloud pub/sub", "google cloud functions",
        "google cloud ai", "vertex ai", "google bigquery",
        "azure", "microsoft azure", "azure app service",
        "azure functions", "azure storage", "azure sql",
        "azure cosmos db", "azure devops", "azure kubernetes service",
        "heroku", "netlify", "vercel", "railway", "render",
        "docker", "containerization", "containers", "docker containers",
        "docker images", "dockerfile", "docker compose", "docker swarm",
        "container registry", "docker hub", "ecr", "gcr",
        "kubernetes", "k8s", "container orchestration",
        "kubernetes deployment", "kubernetes service", "kubernetes ingress",
        "kubernetes pods", "kubernetes namespace", "kubernetes volumes",
        "kubernetes scaling", "kubernetes monitoring", "kubectl",
        "helm", "kubernetes package manager", "helm charts",
        "service mesh", "istio", "linkerd", "consul",
        "terraform", "infrastructure as code", "iac", "terraform modules",
        "cloudformation", "aws cloudformation", "arm templates",
        "ansible", "configuration management", "playbooks",
        "chef", "puppet", "salt", "provisioning",
        "ci/cd", "continuous integration", "continuous deployment",
        "continuous delivery", "build pipeline", "deployment pipeline",
        "github actions", "github workflow", "gitlab ci", "gitlab ci/cd",
        "jenkins", "circleci", "travis ci", "appveyor",
        "gitlab runner", "github runner", "jenkins pipeline",
        "build automation", "test automation", "deployment automation",
        "git workflow", "branching strategy", "git flow",
        "devops", "devops practices", "site reliability engineering", "sre",
        "monitoring", "observability", "logging", "tracing", "metrics",
        "datadog", "new relic", "elastic", "splunk", "sumo logic",
        "prometheus", "grafana", "kibana", "graylog",
        "alerting", "incident management", "on-call", "pagerduty",
        "linux", "unix", "bash", "shell scripting", "bash scripting",
        "zsh", "fish", "powershell", "system administration",
        "networking", "dns", "tcp/ip", "http", "https",
        "ssl/tls", "certificates", "firewall", "network security",
        "vpn", "proxy", "load balancing", "rate limiting",
        "autoscaling", "auto-scaling", "horizontal scaling",
        "vertical scaling", "scalability", "high availability",
        "disaster recovery", "backup", "recovery", "rto", "rpo",
        "database backup", "data backup", "incremental backup",
        "zero-downtime deployment", "blue-green deployment",
        "canary deployment", "rolling deployment", "rollback"
    ],

    # ────────────────────────────────────────────────────────────
    "ai_ml": [
        "machine learning", "ml", "deep learning", "dl",
        "supervised learning", "unsupervised learning", "reinforcement learning",
        "neural networks", "artificial neural networks", "ann",
        "convolutional neural networks", "cnn", "recurrent neural networks", "rnn",
        "lstm", "gru", "transformer", "attention mechanism",
        "nlp", "natural language processing", "language model",
        "llm", "large language model", "gpt", "bert", "t5",
        "generative ai", "gen ai", "text generation", "image generation",

        # ── LLM models ──────────────────────────────────────────
        "llama", "llama2", "llama3", "llama-3", "llama 3",
        "mistral", "mixtral",
        "claude", "claude 3", "claude-3",
        "gpt-4", "gpt-3.5", "gpt4", "gpt 4",
        "gemini", "gemini pro", "gemini ultra",
        "palm", "palm2", "palm 2",
        "falcon", "vicuna", "alpaca", "dolly",
        "phi", "phi-2", "phi-3",

        # ── GenAI Frameworks ────────────────────────────────────
        "langchain", "lang chain",
        "llamaindex", "llama index", "llama-index",
        "haystack", "deepset haystack",
        "crewai", "crew ai",
        "autogen", "auto gen",
        "dspy", "dsp", "stanford dspy",
        "semantic kernel",
        "guidance", "outlines",
        "instructor", "marvin",

        # ── Prompt engineering ──────────────────────────────────
        "prompt engineering", "prompt design", "prompt optimization",
        "chain of thought", "chain-of-thought", "cot prompting",
        "few-shot", "few shot", "few-shot prompting",
        "zero-shot", "zero shot", "zero-shot prompting",
        "system prompt", "prompt template",
        "prompt tuning", "prefix tuning", "p-tuning",
        "in-context learning", "icl",

        # ── RAG & Retrieval ─────────────────────────────────────
        "rag", "retrieval augmented generation",
        "vector database", "vector db", "vector store",
        "pinecone", "weaviate", "chromadb", "chroma",
        "milvus", "qdrant", "pgvector",
        "faiss", "annoy", "hnsw",
        "semantic search", "hybrid search", "dense retrieval",
        "bm25", "sparse retrieval", "re-ranking", "reranking",

        # ── Embeddings ──────────────────────────────────────────
        "embeddings", "embedding", "text embeddings",
        "word embedding", "sentence embedding", "text embedding",
        "word2vec", "glove", "fasttext",
        "sentence transformers", "bi-encoder", "cross-encoder",
        "openai embeddings", "ada embeddings",

        # ── Fine-tuning ─────────────────────────────────────────
        "fine-tuning", "finetuning", "fine tuning",
        "lora", "low-rank adaptation", "low rank adaptation",
        "qlora", "quantized lora",
        "peft", "parameter efficient fine-tuning",
        "sft", "supervised fine-tuning",
        "rlhf", "reinforcement learning from human feedback",
        "dpo", "direct preference optimization",
        "instruction tuning", "instruction following",
        "full fine-tuning", "domain adaptation",

        # ── LLM Deployment & Serving ────────────────────────────
        "vllm", "v-llm",
        "ollama",
        "litellm", "lite llm",
        "triton inference server", "triton",
        "text generation inference", "tgi",
        "openai api", "anthropic api", "huggingface api",
        "model serving", "model deployment", "llm deployment",
        "api endpoint", "inference endpoint",
        "quantization", "gguf", "ggml", "gptq", "awq",
        "model compression", "model optimization",

        # ── LLM Evaluation ──────────────────────────────────────
        "ragas", "rag evaluation",
        "trulens", "tru lens",
        "langsmith", "lang smith",
        "deepeval", "deep eval",
        "promptfoo",
        "llm evaluation", "model evaluation",
        "hallucination detection", "factuality",

        # ── Agents & Multi-agent ────────────────────────────────
        "agentic", "ai agents", "llm agents",
        "tool calling", "tool use", "function calling",
        "multi-agent", "multi agent", "agent orchestration",
        "autonomous agents", "react agent", "plan and execute",
        "memory", "long-term memory", "short-term memory",
        "agent memory", "working memory",

        # ── HuggingFace ecosystem ───────────────────────────────
        "huggingface", "hugging face", "huggingface transformers",
        "transformers library", "diffusers", "datasets library",
        "accelerate", "peft library", "trl", "bitsandbytes",
        "huggingface hub", "model hub",

        # ── MLOps ───────────────────────────────────────────────
        "mlops", "ml operations", "ml engineering", "ml pipeline",
        "feature store", "data versioning", "model versioning",
        "experiment tracking", "mlflow", "weights and biases",
        "wandb", "neptune", "comet ml",
        "model registry", "model monitoring", "model drift",
        "data drift", "concept drift",
        "kubeflow", "sagemaker", "vertex ai pipeline",
        "zenml", "bentoml", "seldon", "kserve",

        # ── Classic ML ──────────────────────────────────────────
        "tensorflow", "keras", "pytorch", "torch", "fastai",
        "scikit-learn", "sklearn", "xgboost", "lightgbm", "catboost",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn",
        "plotly", "visualization", "data visualization",
        "jupyter", "jupyter notebook", "ipython", "colab",
        "anaconda", "miniconda", "conda", "pip",
        "feature engineering", "feature extraction", "feature selection",
        "model evaluation", "cross validation", "hyperparameter tuning",
        "computer vision", "image classification", "object detection",
        "segmentation", "pose estimation", "face recognition",
        "ocr", "optical character recognition", "text recognition",
        "audio processing", "speech recognition", "speech synthesis",
        "time series", "forecasting", "anomaly detection",
        "clustering", "classification", "regression",
        "decision trees", "random forest", "gradient boosting",
        "svm", "support vector machine", "naive bayes", "knn",
        "ensemble learning", "bagging", "boosting", "stacking",
        "dimensionality reduction", "pca", "tsne", "umap",
        "optimization", "gradient descent", "adam optimizer",
        "loss function", "accuracy", "precision", "recall", "f1",
        "roc", "auc", "confusion matrix", "metrics"
    ],

    # ────────────────────────────────────────────────────────────
    "data_engineering": [
        "data pipeline", "etl", "extract transform load", "elt",
        "apache spark", "spark", "pyspark", "spark sql", "spark streaming",
        "hadoop", "mapreduce", "hdfs", "hive", "pig",
        "kafka", "apache kafka", "message queue", "pub/sub",
        "rabbitmq", "activemq", "aws sqs", "gcp pubsub",
        "airflow", "apache airflow", "dag", "workflow orchestration",
        "dbt", "data build tool", "data transformation", "analytics engineering",
        "luigi", "prefect", "dagster", "nextflow",
        "snowflake", "snowflake cloud", "snowflake warehouse",
        "bigquery", "google bigquery", "data warehouse", "data lake",
        "redshift", "amazon redshift", "aws data warehouse",
        "synapse", "azure synapse", "azure data warehouse",
        "delta lake", "apache delta", "iceberg", "hudi",
        "data modeling", "dimensional modeling", "fact table", "dimension table",
        "star schema", "snowflake schema", "data mart",
        "sql", "sql optimization", "query performance",
        "data quality", "data validation", "data testing",
        "data governance", "metadata", "data catalog", "lineage",
        "data security", "encryption", "access control",
        "data privacy", "gdpr", "ccpa", "data anonymization",
        "streaming", "real-time processing", "stream processing",
        "flink", "apache flink", "beam", "apache beam", "samza",
        "data ingestion", "change data capture", "cdc", "log capture",
        "rest api ingestion", "webhook", "batch processing",
        "incremental processing", "delta processing", "change tracking",
        "data formats", "parquet", "orc", "avro", "protobuf",
        "json", "csv", "xml", "data serialization",
        "compression", "gzip", "snappy", "lz4", "zstd",
        "data integration", "master data management", "mdm",
        "api integration", "database integration", "file integration",
        "data monitoring", "data observability", "data health"
    ],

    # ────────────────────────────────────────────────────────────
    "testing_qa": [
        "testing", "software testing", "qa", "quality assurance",
        "unit testing", "unit test", "jest", "vitest", "pytest",
        "unittest", "nunit", "junit", "testng",
        "integration testing", "integration test", "api testing",
        "end-to-end testing", "e2e testing", "e2e test",
        "functional testing", "regression testing", "smoke testing",
        "sanity testing", "acceptance testing", "user acceptance testing", "uat",
        "performance testing", "load testing", "stress testing",
        "scalability testing", "endurance testing", "volume testing",
        "jmeter", "locust", "k6", "gatling", "wrk",
        "security testing", "penetration testing", "vulnerability scanning",
        "owasp testing", "burp suite", "zaproxy",
        "test-driven development", "tdd", "behavior-driven development", "bdd",
        "test automation", "automated testing", "test framework",
        "cypress", "playwright", "selenium", "webdriver", "puppeteer",
        "nightwatch", "testcafe", "protractor",
        "mocha", "chai", "jasmine", "cucumber", "gherkin",
        "testing library", "react testing library", "enzyme",
        "mock", "mocking", "stub", "spy", "mock framework",
        "sinon", "jest mocks", "unittest.mock",
        "code coverage", "coverage report", "lcov", "codecov",
        "test data", "test fixtures", "test setup", "test teardown",
        "assertions", "assertion library", "chai assertions",
        "test reporting", "test results", "ci/cd testing",
        "pre-commit hooks", "lint-staged", "husky"
    ],

    # ────────────────────────────────────────────────────────────
    "version_control": [
        "git", "version control", "git version control", "distributed version control",
        "github", "gitlab", "bitbucket", "gitea",
        "github repository", "gitlab repository", "git repository",
        "git commands", "git clone", "git push", "git pull",
        "git commit", "git branch", "git merge", "git rebase",
        "git stash", "git cherry-pick", "git revert", "git reset",
        "git workflow", "git flow", "trunk-based development",
        "feature branch", "release branch", "hotfix branch",
        "merge conflict", "conflict resolution", "merge strategy",
        "pull request", "pr", "merge request", "code review",
        "git hooks", "pre-commit", "husky", "lint-staged",
        "github actions", "workflow automation", "ci/cd automation",
        "semantic versioning", "version tagging", "release management",
        "git submodules", "monorepo", "git sparse checkout",
        "github pages", "github wiki", "documentation",
        "git credentials", "ssh keys", "personal access token",
        "git rebasing", "interactive rebase", "squashing commits",
        "git diff", "git patch", "comparing versions"
    ],

    # ────────────────────────────────────────────────────────────
    "software_engineering": [
        "software development", "software engineering", "programming",
        "code quality", "clean code", "code standards", "coding standards",
        "design patterns", "creational patterns", "structural patterns",
        "behavioral patterns", "gang of four", "gof patterns",
        "singleton", "factory", "builder", "observer", "strategy",
        "adapter", "decorator", "facade", "proxy", "chain of responsibility",
        "solid principles", "single responsibility", "open closed",
        "liskov substitution", "interface segregation", "dependency inversion",
        "dry", "don't repeat yourself", "kiss", "yagni",
        "refactoring", "code refactoring", "technical debt",
        "software architecture", "system architecture", "architecture design",
        "scalability", "scalable design", "horizontal scaling",
        "vertical scaling", "performance optimization", "optimization",
        "algorithms", "data structures", "algorithm analysis",
        "big o", "time complexity", "space complexity",
        "sorting", "searching", "graph algorithms", "dynamic programming",
        "system design", "distributed systems", "microservices",
        "monolithic architecture", "service-oriented architecture", "soa",
        "asynchronous programming", "async/await", "promises", "callbacks",
        "concurrent programming", "threading", "multiprocessing",
        "locks", "semaphores", "mutexes", "race conditions",
        "deadlock", "synchronization", "thread safety",
        "error handling", "exception handling", "error recovery",
        "logging", "debug logging", "trace logging", "error logging",
        "documentation", "code documentation", "api documentation",
        "comments", "javadoc", "docstring", "markdown",
        "naming conventions", "camelcase", "snake_case", "kebab-case",
        "code organization", "project structure", "folder structure",
        "modularity", "loose coupling", "high cohesion",
        "dependency management", "package management", "dependency injection",
        "ioc", "inversion of control", "service locator",
        "design review", "code review", "peer review", "architecture review",
        "performance profiling", "memory profiling", "cpu profiling",
        "benchmarking", "load testing", "stress testing",
        "security best practices", "secure coding", "owasp top 10",
        "secure design", "threat modeling", "risk assessment"
    ],

    # ────────────────────────────────────────────────────────────
    "soft_skills": [
        "communication", "verbal communication", "written communication",
        "presentation", "public speaking", "storytelling",
        "teamwork", "collaboration", "cooperation", "team player",
        "leadership", "team leadership", "technical leadership",
        "mentoring", "coaching", "knowledge sharing", "teaching",
        "problem solving", "analytical thinking", "critical thinking",
        "decision making", "judgment", "reasoning",
        "time management", "prioritization", "multitasking",
        "project management", "agile", "scrum", "kanban",
        "sprint planning", "estimation", "velocity",
        "product management", "user stories", "requirements gathering",
        "stakeholder management", "communication with stakeholders",
        "customer service", "customer support", "user support",
        "attention to detail", "accuracy", "precision", "quality focus",
        "adaptability", "flexibility", "learning agility", "quick learner",
        "resilience", "perseverance", "persistence", "dedication",
        "curiosity", "continuous learning", "self-improvement",
        "creativity", "innovation", "thinking outside the box",
        "negotiation", "conflict resolution", "mediation",
        "empathy", "emotional intelligence", "interpersonal skills",
        "professionalism", "reliability", "accountability", "responsibility",
        "integrity", "honesty", "ethics", "ethical behavior"
    ]
}

# ────────────────────────────────────────────────────────────
# Build ALL_SKILLS list
ALL_SKILLS = []
for category, skills in SKILL_TAXONOMY.items():
    ALL_SKILLS.extend(skills)

# Remove duplicates while preserving order
ALL_SKILLS = list(dict.fromkeys(ALL_SKILLS))

# Build SKILL_TO_CATEGORY mapping
SKILL_TO_CATEGORY = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        SKILL_TO_CATEGORY[skill.lower()] = category


# ────────────────────────────────────────────────────────────
# PUBLIC FUNCTIONS
def get_all_skills():
    """Return list of all skills in the taxonomy."""
    return ALL_SKILLS


def get_skill_category(skill: str) -> str:
    """Get the category for a given skill."""
    return SKILL_TO_CATEGORY.get(skill.lower(), "other")


def get_taxonomy():
    """Return the complete skill taxonomy."""
    return SKILL_TAXONOMY


def get_category_skills(category: str):
    """Get all skills in a specific category."""
    return SKILL_TAXONOMY.get(category, [])


# ────────────────────────────────────────────────────────────
# TEST/DEBUG
if __name__ == "__main__":
    print("=" * 70)
    print("SKILL TAXONOMY SUMMARY")
    print("=" * 70)

    total_skills = len(get_all_skills())
    print(f"\n✅ Total skills in taxonomy: {total_skills}\n")

    for category, skills in SKILL_TAXONOMY.items():
        print(f"  📌 {category.upper().replace('_', ' ')}: {len(skills)} skills")

    print(f"\n" + "=" * 70)
    print(f"Sample skills extraction:")
    print(f"=" * 70)

    test_skills = ["html5", "react", "node.js", "python", "aws", "leadership",
                   "langchain", "llm", "rag", "fine-tuning", "lora", "vllm"]
    for skill in test_skills:
        category = get_skill_category(skill)
        print(f"  ✓ '{skill}' → {category}")

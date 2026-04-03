# nlp/skill_ner.py

import re
from typing import List, Dict
from skill_taxonomy import get_all_skills, get_skill_category, SKILL_TAXONOMY

# ── Alias map: resume words → canonical taxonomy skill ───────
# If a resume says "react.js" or "reactjs", treat it as "react"
SKILL_ALIASES = {
    "react":            ["react.js", "reactjs", "react js"],
    "vue.js":           ["vue", "vuejs", "vue js"],
    "angular":          ["angular.js", "angularjs"],
    "next.js":          ["nextjs", "next js"],
    "nuxt.js":          ["nuxtjs", "nuxt js"],
    "node.js":          ["nodejs", "node js"],
    "express":          ["express.js", "expressjs"],
    "nest.js":          ["nestjs"],
    "rest api":         ["rest", "restful", "rest apis", "restful api", "restful apis"],
    "graphql":          ["graph ql"],
    "ci/cd":            ["ci cd", "cicd", "ci-cd"],
    "github actions":   ["github-actions", "gh actions"],
    "websockets":       ["web sockets", "websocket", "web socket"],
    "postgresql":       ["postgres", "psql"],
    "mongodb":          ["mongo db", "mongo"],
    "tailwind css":     ["tailwind", "tailwindcss"],
    "typescript":       ["ts"],
    "javascript":       ["js", "es6", "es2015"],
    "machine learning": ["ml"],
    "deep learning":    ["dl"],
    "docker":           ["docker containers", "containerization"],
    "kubernetes":       ["k8s"],
    "aws":              ["amazon web services", "amazon aws"],
    "gcp":              ["google cloud", "google cloud platform"],
    "langchain":        ["lang chain"],
    "llamaindex":       ["llama index", "llama-index"],
    "crewai":           ["crew ai", "crew-ai"],
    "huggingface":      ["hugging face", "hf", "hugging-face"],
    "fine-tuning":      ["finetuning", "fine tuning", "finetune"],
    "lora":             ["low-rank adaptation", "low rank adaptation"],
    "qlora":            ["quantized lora", "q-lora"],
    "peft":             ["parameter efficient fine-tuning"],
    "rag":              ["retrieval augmented generation", "retrieval-augmented generation"],
    "embeddings":       ["embedding", "text embeddings", "word embeddings"],
    "vllm":             ["v-llm", "v llm"],
    "litellm":          ["lite llm", "lite-llm"],
    "openai api":       ["openai", "open ai api", "chatgpt api"],
    "vector database":  ["vector db", "vectordb", "vector store"],
    "llm":              ["large language model", "large language models"],
    "agentic":          ["ai agents", "llm agents", "autonomous agents"],
    "tool calling":     ["tool use", "function calling"],
    "ragas":            ["rag evaluation", "rag eval"],
    "langsmith":        ["lang smith"],
    "gpt-4":            ["gpt4", "gpt 4", "openai gpt-4"],
    "llama":            ["llama2", "llama3", "llama-3", "llama 3", "meta llama"],
    "mistral":          ["mixtral"],
    "gemini":           ["google gemini", "gemini pro"],
    "haystack":         ["deepset haystack"],
    "dspy":             ["stanford dspy"],
}

# Build reverse map: alias → canonical
ALIAS_TO_CANONICAL = {}
for canonical, aliases in SKILL_ALIASES.items():
    for alias in aliases:
        ALIAS_TO_CANONICAL[alias.lower()] = canonical.lower()


class SkillExtractor:
    def __init__(self):
        self.all_skills = get_all_skills()
        # Sort by length (longest first) to match multi-word skills first
        self.all_skills_sorted = sorted(self.all_skills, key=len, reverse=True)
        print(f"✅ SkillExtractor initialized with {len(self.all_skills)} skills")

    def extract_skills(self, text: str) -> Dict:
        """
        Extract skills from resume or job description text.
        Returns dict with matched skills and their categories.
        """
        text_lower = text.lower()

        # ── Step 1: Replace aliases in text before matching ──
        # e.g. "react.js" → "react", "nodejs" → "node.js"
        # Sort aliases longest-first to avoid partial replacements
        for alias, canonical in sorted(ALIAS_TO_CANONICAL.items(), key=lambda x: -len(x[0])):
            pattern = r'\b' + re.escape(alias) + r'\b'
            text_lower = re.sub(pattern, canonical, text_lower)

        found_skills = []
        found_skills_set = set()

        # ── Step 2: Match taxonomy skills against normalized text ──
        for skill in self.all_skills_sorted:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                skill_lower = skill.lower()
                if skill_lower not in found_skills_set:
                    found_skills.append(skill)
                    found_skills_set.add(skill_lower)

        result = {
            "skills": found_skills,
            "skill_count": len(found_skills),
            "by_category": self._organize_by_category(found_skills),
            "skill_vector": self._vectorize(found_skills)
        }

        return result

    def _organize_by_category(self, found_skills: List[str]) -> Dict[str, List[str]]:
        """Organize found skills by their categories."""
        by_category = {}
        for skill in found_skills:
            category = get_skill_category(skill)
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill)
        return by_category

    def _vectorize(self, found_skills: List[str]) -> List[int]:
        """
        Convert found skills into a binary vector.
        1 = skill present, 0 = skill absent.
        Used as input features for FL model.
        """
        found_skills_lower = [s.lower() for s in found_skills]
        vector = [
            1 if skill.lower() in found_skills_lower else 0
            for skill in self.all_skills
        ]
        return vector

    def get_skill_gap(self, resume_skills: List[str], required_skills: List[str]) -> Dict:
        """
        Compare resume skills vs required skills.
        Returns missing skills and match percentage.

        ── Fix: normalize both sets before comparing ──
        Strips ".js" suffixes and spaces so "react.js" == "react",
        "node.js" == "nodejs", "rest api" == "rest" etc.
        """
        def normalize(s: str) -> str:
            s = s.lower().strip()
            # Remove common suffixes that shouldn't affect matching
            s = re.sub(r'\.js$', '', s)
            s = re.sub(r'\s+', ' ', s)
            return s

        # Build normalized → original mapping for resume skills
        resume_norm = {}
        for s in resume_skills:
            resume_norm[normalize(s)] = s.lower()

        # Also add alias expansions to resume set
        resume_norm_set = set(resume_norm.keys())
        for alias, canonical in ALIAS_TO_CANONICAL.items():
            if normalize(alias) in resume_norm_set:
                resume_norm_set.add(normalize(canonical))
            if normalize(canonical) in resume_norm_set:
                resume_norm_set.add(normalize(alias))

        required_norm = {normalize(s): s for s in required_skills}

        matched_norm  = set(resume_norm_set) & set(required_norm.keys())
        missing_norm  = set(required_norm.keys()) - set(resume_norm_set)

        matched = [required_norm[n] for n in matched_norm]
        missing = [required_norm[n] for n in missing_norm]
        extra   = [resume_norm[n] for n in (set(resume_norm.keys()) - set(required_norm.keys()))
                   if n in resume_norm]

        match_pct = (len(matched) / len(required_norm) * 100) if required_norm else 0

        return {
            "matched_skills":  matched,
            "missing_skills":  missing,
            "extra_skills":    extra,
            "match_percentage": round(match_pct, 2),
            "total_required":  len(required_norm),
            "total_matched":   len(matched)
        }


# ────────────────────────────────────────────────────────────
# QUICK TEST
if __name__ == "__main__":
    extractor = SkillExtractor()

    sample_resume = """
    Senior Web Developer - 7+ Years Professional Experience

    HTML5 expert, CSS3 expert, JavaScript expert, React.js expert, Vue.js expert,
    Node.js expert, Express.js expert, TypeScript, REST API expert, GraphQL expert,
    PostgreSQL expert, MongoDB expert, Redis expert, Docker expert,
    Kubernetes expert, AWS expert, CI/CD expert, GitHub Actions.

    Progressive Web Apps, service workers, web accessibility, WCAG compliance,
    web performance optimization, Core Web Vitals, Lighthouse, web security,
    OAuth, JWT authentication, responsive design, web design.

    Agile development, Scrum, problem solving, communication, leadership,
    testing, Jest, test-driven development, Git, GitHub, code review,
    software architecture, design patterns, mentoring, technical documentation.
    """

    print("\n" + "=" * 70)
    print("SKILL EXTRACTION TEST")
    print("=" * 70)

    result = extractor.extract_skills(sample_resume)

    print(f"\n📊 Skills Extracted: {len(result['skills'])}")
    print(f"🎯 Skill Vector Length: {len(result['skill_vector'])}")

    print(f"\n✅ Skills by Category:")
    for category, skills in result["by_category"].items():
        print(f"  [{category}]")
        for skill in skills:
            print(f"    • {skill}")

    print(f"\n" + "=" * 70)
    print("SKILL GAP ANALYSIS TEST")
    print("=" * 70)

    required = [
        "html5", "css3", "javascript", "react", "node.js",
        "express", "rest api", "postgresql", "docker", "kubernetes",
        "aws", "git", "ci/cd", "web design", "responsive design"
    ]

    gap = extractor.get_skill_gap(result["skills"], required)

    print(f"\n✅ Matched Skills ({len(gap['matched_skills'])}):")
    for skill in gap['matched_skills']:
        print(f"    • {skill}")

    print(f"\n❌ Missing Skills ({len(gap['missing_skills'])}):")
    for skill in gap['missing_skills']:
        print(f"    • {skill}")

    print(f"\n📈 Match Percentage: {gap['match_percentage']}%")
    print(f"🎯 Total Matched: {gap['total_matched']}/{gap['total_required']}")

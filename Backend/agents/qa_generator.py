# Backend/agents/qa_generator.py
from __future__ import annotations
from typing import Dict, Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from config import Config

# XP → tier mapping
TIER_MAP = {
    "simple":   {"difficulty": "easy",   "time_s": 35, "xp_min": 0,   "xp_max": 35},
    "moderate": {"difficulty": "medium", "time_s": 45, "xp_min": 36,  "xp_max": 120},
    "advanced": {"difficulty": "hard",   "time_s": 60, "xp_min": 121, "xp_max": 999999},
}

ALLOWED_TACTICS = ["Reconnaissance", "Initial Access", "Execution", "Privilege Escalation"]

SYSTEM_BASE = (
    "You are a cybersecurity training question generator.\n"
    "Output STRICT JSON with keys: question, choices, answer_key, explanation, tags, difficulty, estimated_time_s.\n"
    "Rules:\n"
    "- Exactly 1 multiple-choice question with exactly 4 options.\n"
    "- Only ONE correct answer; answer_key MUST be one of A|B|C|D.\n"
    "- Keep content training-safe (no exploit code, payloads, PoCs, live IOCs).\n"
    "- Tie content to the given MITRE tactic/technique.\n"
)

USER_TMPL = """\
Tactic: {tactic}
Technique: {technique}

Target difficulty: {difficulty_label}

Generate 1 multiple-choice question tied to this tactic/technique.
Keep the stem concise; explanations must say why the correct choice is right and the others are wrong.

Return ONLY JSON, e.g.:
{{
  "question": "…?",
  "choices": ["Option A","Option B","Option C","Option D"],
  "answer_key": "A",
  "explanation": "Why A is correct; why others are plausible but wrong.",
  "tags": ["ATT&CK:{tech_tag}", "ATT&CK:{tactic_tag}"],
  "difficulty": "{difficulty_label}",
  "estimated_time_s": {time_s}
}}
"""

def _tier_for_xp(xp: int) -> str:
    if xp <= 35: return "simple"
    if xp <= 120: return "moderate"
    return "advanced"

def generate_question(
    tactic: str,
    technique_id: Optional[str],
    xp: int,
    *,
    model: str = "gemini-1.5-flash",   # fast & cheap; switch to 'gemini-1.5-pro' for higher quality
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    Generate a single MCQ JSON using Google Gemini.
    """
    if tactic not in ALLOWED_TACTICS:
        raise ValueError(f"Tactic '{tactic}' not allowed. Must be one of {ALLOWED_TACTICS}")

    tier = _tier_for_xp(int(xp))
    cfg = TIER_MAP[tier]

    # LangChain Gemini chat model
    llm = ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=Config.GOOGLE_API_KEY,  # pulled from .env via Config
    )
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_BASE),
        ("user", USER_TMPL),
    ])

    tactic_tag = (tactic or "Unknown").replace(" ", "_")
    tech_tag = technique_id or "NA"

    obj = (prompt | llm | parser).invoke({
        "tactic": tactic,
        "technique": technique_id or "N/A",
        "difficulty_label": cfg["difficulty"],
        "time_s": cfg["time_s"],
        "tactic_tag": tactic_tag,
        "tech_tag": tech_tag,
    })

    # Safeguards / defaults
    obj.setdefault("difficulty", cfg["difficulty"])
    obj.setdefault("estimated_time_s", cfg["time_s"])
    obj.setdefault("tags", [])
    if technique_id and f"ATT&CK:{technique_id}" not in obj["tags"]:
        obj["tags"].append(f"ATT&CK:{technique_id}")
    t_tag_full = f"ATT&CK:{tactic_tag}"
    if t_tag_full not in obj["tags"]:
        obj["tags"].append(t_tag_full)

    # Annotate the tier for the UI
    obj["difficulty_meta"] = {
        "tier": tier,
        "time_s": obj["estimated_time_s"],
        "xp_reward": 5 if tier == "simple" else (8 if tier == "moderate" else 12),
    }
    return obj






























# # qa_generator.py
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser

# TIER_MAP = {
#     "simple":   {"difficulty": "easy",   "time_s": 35, "xp_min": 0,   "xp_max": 35},
#     "moderate": {"difficulty": "medium", "time_s": 45, "xp_min": 36,  "xp_max": 120},
#     "advanced": {"difficulty": "hard",   "time_s": 60, "xp_min": 121, "xp_max": 99999},
# }

# # only allow these MITRE tactics
# ALLOWED_TACTICS = ["Reconnaissance", "Initial Access", "Execution", "Privilege Escalation"]

# SYSTEM_PROMPT = """
# You are a cybersecurity training question generator.
# Rules:
# - Restrict questions to MITRE ATT&CK tactics/techniques provided.
# - Never produce exploit code, PoCs, or live payloads.
# - Each output must be valid JSON: {question, choices, answer_key, explanation, tags, difficulty, estimated_time_s}.
# - Choices must have exactly 4 options, only one correct.
# - Explanation must describe why correct choice is right, and why others are wrong.
# """

# USER_TMPL = """\
# Tactic: {tactic}
# Technique: {technique}

# Target difficulty: {difficulty_label}

# Generate 1 multiple-choice question tied to this tactic/technique.
# """

# def tier_for_xp(xp: int) -> str:
#     for tier, rng in TIER_MAP.items():
#         if rng["xp_min"] <= xp <= rng["xp_max"]:
#             return tier
#     return "simple"

# def generate_question(tactic: str, technique_id: str, xp: int, model="gpt-4o-mini") -> dict:
#     if tactic not in ALLOWED_TACTICS:
#         raise ValueError(f"Tactic {tactic} not allowed. Must be one of {ALLOWED_TACTICS}")

#     tier = tier_for_xp(xp)
#     tier_cfg = TIER_MAP[tier]

#     llm = ChatOpenAI(model=model, temperature=0.3)
#     parser = JsonOutputParser()
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", SYSTEM_PROMPT),
#         ("user", USER_TMPL),
#     ])

#     q = (prompt | llm | parser).invoke({
#         "tactic": tactic,
#         "technique": technique_id or "N/A",
#         "difficulty_label": tier_cfg["difficulty"],
#     })

#     q.setdefault("difficulty", tier_cfg["difficulty"])
#     q.setdefault("estimated_time_s", tier_cfg["time_s"])
#     q["tier"] = tier
#     return q

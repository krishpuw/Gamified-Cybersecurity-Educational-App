# questions.py
from __future__ import annotations
from flask import Blueprint, request, jsonify , render_template
from agents.qa_generator import generate_question
from agents.qa_validator import validate_question
from agents.mitre_map import normalize_tactic, pick_technique, is_valid_technique_for_tactic

# Prefer server-side XP lookup
try:

    from ..agents.userprogress import get_user_xp  
except Exception:
    def get_user_xp(_user_id: int) -> int:
        return 0

questions_bp = Blueprint("questions_bp", __name__)

def _tier_from_xp(xp: int) -> str:
    if xp <= 35: return "simple"
    if xp <= 70: return "moderate"
    return "advanced"

@questions_bp.route("/api/questions/generate7", methods=["POST"])
def generate_batch():
    """
    Body:
    {
      "user_id": 123,           # preferred; server will read XP
      "xp": 0,                  # optional fallback
      "tactic": "Execution",    # optional; normalized if missing
      "technique_id": "T1059"   # optional; enforced to belong to tactic
    }
    """
    b = request.get_json(force=True)

    # Resolve XP
    xp = 0
    if b.get("user_id") is not None:
        try: xp = int(get_user_xp(int(b["user_id"])))
        except Exception: xp = 0
    if xp == 0 and b.get("xp") is not None:
        try: xp = int(b["xp"])
        except Exception: pass

    tactic = normalize_tactic(b.get("tactic")) if b.get("tactic") else normalize_tactic(None)

    technique_id = b.get("technique_id")
    if not technique_id or not is_valid_technique_for_tactic(tactic, technique_id):
        technique_id, _ = pick_technique(tactic)

    items = []
    target = 7
    max_attempts_per_q = 3
    attempts = 0

    while len(items) < target:
        attempts += 1
        if attempts > target * max_attempts_per_q:
            break

        q = generate_question(tactic=tactic, technique_id=technique_id, xp=xp)  # uses Config key internally
        ok = False
        for _ in range(max_attempts_per_q):
            try:
                if validate_question(q):
                    ok = True
                    break
            except Exception:
                pass
            q = generate_question(tactic=tactic, technique_id=technique_id, xp=xp)

        if ok:
            q.setdefault("tags", [])
            t_tag = f"ATT&CK:{tactic.replace(' ', '_')}"
            if t_tag not in q["tags"]: q["tags"].append(t_tag)
            if f"ATT&CK:{technique_id}" not in q["tags"]: q["tags"].append(f"ATT&CK:{technique_id}")
            q["meta"] = {"tactic": tactic, "technique_id": technique_id, "xp": xp, "tier": _tier_from_xp(xp)}
            items.append(q)
        else:
            technique_id, _ = pick_technique(tactic)

    return jsonify({
        "count": len(items),
        "xp": xp,
        "tier": _tier_from_xp(xp),
        "tactic": tactic,
        "technique_id": technique_id,
        "items": items
    }), 200

@questions_bp.route("/questions", methods=["GET"])
def questions_page():
    return render_template("questions.html")


ui_bp = Blueprint("ui_bp", __name__)

# @ui_bp.route("/summary")
# def summary_page():
#     # We'll render the template which will read query params on the client
#     return render_template("summary.html")



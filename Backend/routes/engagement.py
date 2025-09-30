# routes/engagement.py
from flask import Blueprint, request, jsonify
from agents.management import ManagementAgent

engagement_bp = Blueprint("engagement_bp", __name__)
agent = ManagementAgent()

@engagement_bp.route("/api/engagement/update", methods=["POST"])
def engagement_update():
    data = request.get_json(force=True)  # raises if wrong content-type
    user_id = data.get("user_id")
    operation_id = data.get("operation_id")
    question_id = data.get("question_id")
    is_correct = bool(data.get("is_correct", False))
    response_time_ms = data.get("response_time_ms")
    difficulty = data.get("difficulty", "easy")

    result = agent.process_event(
        user_id=user_id,
        operation_id=operation_id,
        question_id=question_id,
        is_correct=is_correct,
        response_time_ms=response_time_ms,
        difficulty=difficulty,
    )

    status = 200 if "error" not in result else 400
    return jsonify(result), status

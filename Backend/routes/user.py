# routes/user.py
from flask import Blueprint, jsonify
from model import User

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/api/user/<int:user_id>/progress", methods=["GET"])
def user_progress(user_id: int):
    u = User.query.get(user_id)
    if not u:
        return jsonify({"error": "user not found"}), 404
    return jsonify({
        "user_id": u.id,
        "username": u.username,
        "level": int(u.level or 1),
        "xp": int(u.xp or 0),
        "score": int(getattr(u, "score", 0)),
        "badges": [ub.badge.name for ub in u.user_badges],
    }), 200

# routes/leaderboard.py
from flask import Blueprint, request, jsonify
from model import User

leaderboard_bp = Blueprint("leaderboard_bp", __name__)

@leaderboard_bp.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    limit = int(request.args.get("limit", 10))
    q = User.query.order_by(User.score.desc(), User.xp.desc(), User.level.desc())
    users = q.limit(limit).all()
    rows = []
    for idx, u in enumerate(users, start=1):
        rows.append({
            "rank": idx,
            "user_id": u.id,
            "username": u.username,
            "score": int(getattr(u, "score", 0)),
            "level": int(u.level or 1),
            "xp": int(u.xp or 0),
        })
    return jsonify(rows), 200

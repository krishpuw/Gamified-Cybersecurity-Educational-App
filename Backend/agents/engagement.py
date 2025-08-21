from flask import Blueprint, request, jsonify
engagement_bp = Blueprint("engagement_bp", __name__)

@engagement_bp.route("/api/engagement/update", methods=["POST"])
def engagement_update():
    _ = request.get_json(force=True)
    return jsonify({"ok": True}), 200
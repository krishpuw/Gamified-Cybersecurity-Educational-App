from flask import Blueprint, request, jsonify, session
from agents.attack_agent import AttackAgent
from config import Config

attack_bp = Blueprint("attack_bp", __name__)

# Initialize your AttackAgent with Caldera settings
agent = AttackAgent(Config.CALDERA_URL, Config.API_KEY)

@attack_bp.route("/start-attack", methods=["POST"])
def start_attack():
    data = request.get_json() or {}
    adversary_id = data.get("adversary_id")
    username = session.get("username", "unknown")

    # Auto-generate adversary if not provided
    if not adversary_id:
        objectives = agent.get_all_objectives()
        abilities = agent.get_all_abilities()

        if not objectives or not abilities:
            return jsonify({"error": "Unable to fetch objectives or abilities"}), 500

        default_objective_id = objectives[0]["id"]
        ability_ids = [a["id"] for a in abilities[:3]]  # Pick top 3 or adjust logic

        adversary = agent.create_adversary(
            name=f"adversary_for_{username}",
            description="Auto-generated adversary for attack simulation",
            objective_id=default_objective_id,
            ability_ids=ability_ids
        )

        if not adversary:
            return jsonify({"error": "Failed to create adversary"}), 500

        adversary_id = adversary["id"]

    # Start the Caldera operation
    result = agent.start_attack(adversary_id=adversary_id, username=username)

    if result:
        return jsonify({
            "operation_id": result.get("id"),
            "message": "Attack started successfully."
        }), 200
    else:
        return jsonify({"error": "Failed to start attack"}), 500

@attack_bp.route("/attack-status", methods=["GET"])
def attack_status():
    print("[DEBUG] /attack-status hit")
    operation_id = session.get("operation_id")
    print(f"[DEBUG] Retrieved operation_id: {operation_id}")
    if not operation_id:
        return jsonify({"error": "No active operation found"}), 400
    

@attack_bp.route("/attack-status/<operation_id>")
def attack_status_by_id(operation_id):
    status = agent.get_operation_status(operation_id)
    return jsonify(status or {"error": "not found"}), (200 if status else 404)




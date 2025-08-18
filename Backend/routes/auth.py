from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from model import db, User
from config import Config
from agents.attack_agent import AttackAgent
import bcrypt

auth_bp = Blueprint("auth", __name__)
agent = AttackAgent(Config.CALDERA_URL, Config.API_KEY)

# Landing
@auth_bp.route("/", methods=["GET"])
def button():
    return render_template("landing.html")

# Login (single handler for GET + POST)
@auth_bp.route("/login", methods=["GET", "POST"])
def login_submit():
    if request.method == "GET":
        return render_template("login.html")

    # POST
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login_submit"))

    # Put essentials in session
    session["user_id"] = user.id
    session["username"] = user.username
    # If your User model has xp/level, you can also cache it in session if you like:
    # session["xp"] = getattr(user, "xp", 0)

    # --- Caldera bootstrap (best-effort) ---
    try:
        # 1) Pull objectives/abilities
        objectives = agent.get_all_objectives()
        abilities = agent.get_all_abilities()
        if not objectives or not abilities:
            raise Exception("Missing objectives or abilities")

        default_objective = objectives[0]["id"]
        ability_ids = [a["ability_id"] for a in abilities[:3]]

        # 2) Create adversary
        adversary = agent.create_adversary(
            name=f"adversary_for_{username}",
            description="Auto-generated adversary for simulation",
            objective_id=default_objective,
            ability_ids=ability_ids,
        )
        if not adversary:
            raise Exception("Failed to create adversary")

        # 3) Start attack (may fail depending on env)
        result = agent.start_attack(adversary_id=adversary["adversary_id"], username=username)
        if not result or "id" not in result:
            raise Exception("Failed to start attack")

        # Store operation ID for /game & /attack/status/<id>
        session["operation_id"] = result["id"]

    except Exception as e:
        # Don’t block login if Caldera bootstrap fails—just log and carry on
        print(f"[ERROR] Attack error: {e}")

    flash(f"Welcome, {username}!", "success")
    return redirect(url_for("auth.game_page"))

# Registration
@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password are required.", "error")
        return redirect(url_for("auth.register_page"))

    if User.query.filter_by(username=username).first():
        flash("Username already exists. Please choose another.", "error")
        return redirect(url_for("auth.register_page"))

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! Please log in.", "success")
    return redirect(url_for("auth.login_submit"))

# Game page (now passes user_id and xp to template)
@auth_bp.route("/game", methods=["GET"])
def game_page():
    uid = session.get("user_id")
    username = session.get("username", "Agent")
    operation_id = session.get("operation_id")  # could be None if attack didn’t start

    # Pull XP from DB (default 0 if you don’t track it yet)
    xp = 0
    if uid:
        u = User.query.get(uid)
        if u and hasattr(u, "xp"):
            xp = u.xp or 0

    return render_template(
        "game.html",
        username=username,
        operation_id=operation_id,
        user_id=uid,
        xp=xp,
    )

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from model import db, User
from config import Config
from agents.attack_agent import AttackAgent
import bcrypt

auth_bp = Blueprint("auth", __name__)
agent = AttackAgent(Config.CALDERA_URL, Config.API_KEY)


@auth_bp.route('/', methods=["GET"])
def button():
    return render_template("landing.html")


@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template('login.html')


@auth_bp.route("/login", methods=["GET", "POST"])
def login_submit():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login_submit"))

    session['user_id'] = user.id
    session['username'] = user.username

    try:
        # Step 1: Get objectives and abilities
        objectives = agent.get_all_objectives()
        abilities = agent.get_all_abilities()
        if not objectives or not abilities:
            raise Exception("Missing objectives or abilities")

        # Step 2: Create adversary
        default_objective = objectives[0]["id"]
        ability_ids = [a["id"] for a in abilities[:3]]

        adversary = agent.create_adversary(
            name=f"adversary_for_{username}",
            description="Auto-generated adversary for simulation",
            objective_id=default_objective,
            ability_ids=ability_ids
        )
        if not adversary:
            raise Exception("Failed to create adversary")

        # Step 3: Start attack
        result = agent.start_attack(adversary_id=adversary["id"], username=username)
        if not result or "id" not in result:
            raise Exception("Failed to start attack")

        # Store operation ID for /game
        session['operation_id'] = result["id"]
        print(f"[DEBUG] operation_id = {session['operation_id']}")

    except Exception as e:
        print(f"[ERROR] Attack error: {e}")
        flash("Error starting the attack", "error")
        return redirect(url_for("auth.login_submit"))

    flash(f"Welcome, {username}!", "success")
    return redirect(url_for("auth.game_page"))

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if User.query.filter_by(username=username).first():
        flash("Username already exists. Please choose another.", "error")
        return redirect(url_for('auth.register_page'))

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    flash("Registration successful! Please log in.", "success")
    return redirect(url_for('auth.login_page'))


@auth_bp.route("/game")
def game_page():
    if "operation_id" not in session:
        flash("Attack not started yet", "error")
        return redirect(url_for("auth.login_submit"))

    return render_template(
        "game.html",
        username=session["username"],
        operation_id=session["operation_id"]
    )
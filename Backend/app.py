# app.py

from flask import Flask
from config import Config
from model import db 
import os 
from routes.auth import auth_bp
from routes.attack import attack_bp
from routes.questions import questions_bp
from agents.engagement import engagement_bp

template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FrontEnd')) # to get the Landing page from frontend dir
def create_app():
    app = Flask(__name__, template_folder=template_path) #grabbing 
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(attack_bp, url_prefix="/attack")
    app.register_blueprint(questions_bp)
    app.register_blueprint(engagement_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()


    app.run(debug=True)

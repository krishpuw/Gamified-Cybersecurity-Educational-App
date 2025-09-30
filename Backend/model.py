from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer, default=0)

# better to convert into dictionary and then extract it and using the data for the attacks {ID} and also for the ai models to work on it 
# keep track of the data base 


class Badge(db.Model):
    __tablename__ = "badges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(255), nullable=True)  # optional URL/path

class UserBadge(db.Model):
    __tablename__ = "user_badges"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey("badges.id"), nullable=False)
    awarded_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("User", backref=db.backref("user_badges", lazy="dynamic"))
    badge = db.relationship("Badge")

class EngagementLog(db.Model):
    __tablename__ = "engagement_log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    operation_id = db.Column(db.String(64), nullable=True)   # Caldera op
    question_id = db.Column(db.String(64), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    response_time_ms = db.Column(db.Integer, nullable=True)
    difficulty = db.Column(db.String(16), nullable=True)     # "easy"|"medium"|"hard"
    xp_delta = db.Column(db.Integer, nullable=False, default=0)
    score_delta = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("User", backref=db.backref("engagements", lazy="dynamic"))

from ..models.db import db

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    strava_id = db.Column(db.String(50), nullable=True)
    strava_token = db.Column(db.String(200), nullable=True)
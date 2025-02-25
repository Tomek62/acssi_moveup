from ..models.db import db

# Models
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=True)
    username = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(150), nullable=True)
    strava_id = db.Column(db.String(50), nullable=True)
    strava_access_token = db.Column(db.String(200), nullable=True)
    strava_refresh_token = db.Column(db.String(200), nullable=True)
    strava_expires_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
        }



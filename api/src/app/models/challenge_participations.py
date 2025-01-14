from ..models.db import db

class ChallengeParticipation(db.Model):
    challenge_participation_id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.challenge_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    progress_distance = db.Column(db.Float)
    progress_duration = db.Column(db.Interval)
    status = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
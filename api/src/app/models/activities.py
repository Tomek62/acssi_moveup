from ..models.db import db

class Activity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    type = db.Column(db.String(150), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Float, nullable=False)
    average_speed = db.Column(db.Float, nullable=False)
    max_speed = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
from flask import Blueprint, request, jsonify,redirect, url_for
from ..models.users import User
from ..models.activities import Activity
from requests_oauthlib import OAuth2Session
from flask_bcrypt import Bcrypt
import os
import jwt
from dotenv import load_dotenv
from ..models.db import db
from datetime import datetime, timedelta
import requests
from ..utils.utils import token_required

load_dotenv()

user_routes = Blueprint("user_routes", __name__)

SECRET_KEY = os.getenv('SECRET_KEY')
STRAVA_API_URL = os.getenv('STRAVA_API_URL')

bcrypt = Bcrypt()

# @token_required
@user_routes.route("/get_user", methods=["GET"])
def get_user():
    data = request.json
    token = data.get('token')
    current_u = User.query.filter_by(strava_access_token=token).first()
    # Retourner les données de l'utilisateur courant
    return jsonify({'user': current_u.to_dict()}), 200


@user_routes.route("/update_user", methods=["PUT"])
@token_required
def update_user(current_u):
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username:
        return jsonify({'message': 'Veuillez remplir tous les champs'}), 400

    current_u.email = email
    current_u.username = username
    if password:
        current_u.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    db.session.commit()

    return jsonify({'message': 'Utilisateur mis à jour !'}), 200

@user_routes.route("/add_performance", methods=["POST"])
@token_required
def add_performance(current_u):
    data = request.json
    name = data.get('name')
    type = data.get('type')
    start_time = data.get('start_time')
    duration = data.get('duration')
    distance = data.get('distance')
    elevation_gain = data.get('elevation_gain')
    average_speed = data.get('average_speed')
    max_speed = data.get('max_speed')
    calories = data.get('calories')
    user_id = data.get('user_id')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

    if not name or not type or not start_time or not duration or not distance:
        return jsonify({'message': 'Veuillez remplir tous les champs'}), 400

    # Convert duration string to timedelta
    hours, minutes, seconds = map(int, duration.split(':'))
    duration_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    activity = Activity(
        name=name,
        type=type,
        start_time=start_time,
        duration=duration_timedelta,
        distance=distance,
        elevation_gain=elevation_gain,
        average_speed=average_speed,
        max_speed=max_speed,
        calories=calories,
        user_id=user_id,
        created_at=created_at,
        updated_at=updated_at
    )
    db.session.add(activity)
    db.session.commit()

    return jsonify({'message': 'Activité ajoutée !'}), 201


@user_routes.route("/get_activities", methods=["GET"])
@token_required
def get_activities(current_u):
    # Retourner les activités de l'utilisateur courant
    activities = Activity.query.filter_by(user_id=current_u.id).all()
    return jsonify({'activities': [activity.to_dict() for activity in activities]}), 200

# @token_required
@user_routes.route("/get_strava_activities", methods=["GET"])
def get_strava_activities(current_u):
    # Récupérer les activités de l'utilisateur sur Strava
    strava_token = current_u.strava_token
    if strava_token:
        headers = { "Authorization": f"Bearer {strava_token}" }

        response = requests.get(f"{STRAVA_API_URL}/athlete/activities", headers=headers)
        if response.status_code == 200:
            return jsonify({'activities': response.json()}), 200
        else:   
            return jsonify({'message': 'Une erreur est survenue'}), 400
    else:
        return jsonify({'message': 'Vous devez connecter votre compte Strava'}), 400


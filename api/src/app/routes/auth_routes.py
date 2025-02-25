from flask import Blueprint, request, jsonify,redirect
from ..models.users import User
from requests_oauthlib import OAuth2Session
from flask_bcrypt import Bcrypt
import os
import jwt
from dotenv import load_dotenv
from ..models.db import db
from datetime import datetime, timedelta
import requests
load_dotenv()

auth_routes = Blueprint("auth_routes", __name__)

SECRET_KEY = os.getenv('SECRET_KEY')
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI')
STRAVA_SCOPE = os.getenv('STRAVA_SCOPE')
STRAVA_AUTH_URL = os.getenv('STRAVA_AUTH_URL')
STRAVA_TOKEN_URL = os.getenv('STRAVA_TOKEN_URL')

bcrypt = Bcrypt()


@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    confirmed_password = data.get('confirmed_password')
    if not '@' in email:
        return jsonify({'message': 'Email invalide'}), 400
    if not password or not confirmed_password or password != confirmed_password:
        return jsonify({'message': 'Les mots de passe ne correspondent pas'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email déjà utilisé'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email,username=username ,password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json  # Récupérer les données de la requête
    email = data.get('email')
    password = data.get('password')

    # Vérifier si l'utilisateur existe
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Générer un token avec l'ID utilisateur
    token = jwt.encode(
        {
            'user_id': user.user_id,  # Inclure l'ID utilisateur
            'exp': datetime.utcnow() + timedelta(hours=1)  # Durée de validité du token
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    # Charger les données de l'utilisateur pour les inclure dans la réponse
    user_data = user.to_dict()  # Méthode sérialisée à créer dans le modèle User

    # Retourner le token et les données utilisateur
    return jsonify({
        'token': token,
        'user': user_data
    }), 200


def refresh_strava_token(user):
    if user.strava_expires_at and user.strava_expires_at < datetime.utcnow():
        response = requests.post(STRAVA_TOKEN_URL, data={
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'refresh_token': user.strava_refresh_token,
            'grant_type': 'refresh_token'
        })
        if response.status_code == 200:
            token_data = response.json()
            user.strava_access_token = token_data['access_token']
            user.strava_refresh_token = token_data['refresh_token']
            user.token_expiry = datetime.fromtimestamp(token_data['expires_at'])
            db.session.commit()
            return user.strava_access_token

    return user.strava_access_token

@auth_routes.route('/strava/auth', methods=['GET'])
def strava_auth():
    strava = OAuth2Session(STRAVA_CLIENT_ID, redirect_uri=STRAVA_REDIRECT_URI, scope=STRAVA_SCOPE)
    auth_url, state = strava.authorization_url(STRAVA_AUTH_URL)
    return  redirect(auth_url)

@auth_routes.route('/strava/callback', methods=['GET'])
def strava_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'message': 'Missing code'}), 400

    token_response = requests.post(f"https://www.strava.com/oauth/token?client_id={STRAVA_CLIENT_ID}&client_secret={STRAVA_CLIENT_SECRET}&code={code}&grant_type=authorization_code")

    if not token_response:
        return jsonify({'message': 'Failed to retrieve access token from Strava'}), 400

    strava_user_id = token_response.json()['athlete']['id']
    user = User.query.filter_by(strava_id=strava_user_id).first()
    username = token_response.json()['athlete']['firstname'] + ' ' + token_response.json()['athlete']['lastname']

    if not user:
        user = User(username=username,strava_id=strava_user_id, strava_access_token=token_response.json()['refresh_token'])
        db.session.add(user)
        db.session.commit()
    if user:
        token = refresh_strava_token(user)
    user_data = user.to_dict()
    streamlit_url = f"http://127.0.0.1:8501?access_token={token}"
    return redirect(streamlit_url)


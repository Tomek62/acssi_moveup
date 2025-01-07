from flask import Blueprint, request, jsonify
from ..models.users import User
from requests_oauthlib import OAuth2Session
from flask_bcrypt import Bcrypt
import os
import jwt
from dotenv import load_dotenv
from ..models.db import db
from datetime import datetime, timedelta
load_dotenv()

auth_routes = Blueprint("auth_routes", __name__)

SECRET_KEY = os.getenv('SECRET_KEY')
# STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
# STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
# STRAVA_REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI')
# STRAVA_SCOPE = os.getenv('STRAVA_SCOPE')
# STRAVA_AUTH_URL = os.getenv('STRAVA_AUTH_URL')
# STRAVA_TOKEN_URL = os.getenv('STRAVA_TOKEN_URL')

bcrypt = Bcrypt()


@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.utcnow() + timedelta(minutes=30)},  # Convertir user.id en string
        SECRET_KEY,
        algorithm="HS256"
        )
        return jsonify({"access_token": token, "token_type": "bearer"}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# @app.route('/strava/auth', methods=['GET'])
# def strava_auth():
#     strava = OAuth2Session(STRAVA_CLIENT_ID, redirect_uri=STRAVA_REDIRECT_URI, scope=STRAVA_SCOPE)
#     auth_url, state = strava.authorization_url(STRAVA_AUTH_URL)
#     return jsonify({'auth_url': auth_url})

# @app.route('/strava/callback', methods=['GET'])
# def strava_callback():
#     code = request.args.get('code')
#     if not code:
#         return jsonify({'message': 'Missing code'}), 400

#     strava = OAuth2Session(STRAVA_CLIENT_ID, redirect_uri=STRAVA_REDIRECT_URI)
#     token = strava.fetch_token(
#         STRAVA_TOKEN_URL,
#         client_secret=STRAVA_CLIENT_SECRET,
#         code=code
#     )

#     strava_user_id = token.get('athlete', {}).get('id')
#     user = User.query.filter_by(strava_id=strava_user_id).first()

#     if not user:
#         user = User(strava_id=strava_user_id, strava_token=token['access_token'])
#         db.session.add(user)
#         db.session.commit()

#     return jsonify({'message': 'Strava linked successfully', 'access_token': token['access_token']}), 200
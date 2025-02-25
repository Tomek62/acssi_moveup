import jwt
from functools import wraps
from flask import request, jsonify
from app.models.users import User
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):                      #wrapper for token auth
    @wraps(f)
    def decorated(*args, **kwargs):
        print("Authorization Header:", request.headers.get("Authorization"))
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            if token.startswith("Bearer "):
                token = token.split("Bearer ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            print("Token:", token)
            data = jwt.decode(token,SECRET_KEY, algorithms="HS256")
            print("Data:", data)
            current_u = User.query.filter_by(username=data['user_id']).first()    
            #identify user, otherwise, return error
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_u, *args, **kwargs)   #previously return f(*args, **kwargs)

    return decorated
import os
from flask import Flask
from dotenv import load_dotenv
from .models.db import db
from .routes.init_routes import init_routes
from flask_jwt_extended import JWTManager

load_dotenv()

def create_app(testing=False):
    """Factory function pour créer l'application Flask."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['TESTING'] = testing
    # Init DB
    db.init_app(app)
    # Enregistrer les routes
    init_routes(app)

    return app
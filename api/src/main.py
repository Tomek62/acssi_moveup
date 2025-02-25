import os
from flask import Flask
from dotenv import load_dotenv
from app.routes.init_routes import init_routes
from app.models.db import db  # Importer l'instance de db

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Créer l'application Flask
app = Flask(__name__)


# Configurer la base de données

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialiser la base de données
db.init_app(app)
with app.app_context():
    # Créer toutes les tables
    db.create_all()


# Initialiser les routes
init_routes(app)

if __name__ == "__main__":
    # app.run(debug=os.getenv("FLASK_DEBUG", False))
    # app.run(host="0.0.0.0", port=80)  # Écoute sur toutes les interfaces, port 80
    app.run(debug=True)  # Écoute sur toutes les interfaces, port 80
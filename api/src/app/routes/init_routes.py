from ..routes.auth_routes import auth_routes
from ..routes.user_routes import user_routes

def init_routes(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(user_routes)
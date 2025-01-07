from ..routes.auth_routes import auth_routes

def init_routes(app):
    app.register_blueprint(auth_routes)
from flask import Flask
from flask_cors import CORS

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_object:
        app.config.from_object(config_object)

    CORS(app)

    # Registering minimal blueprints for app to work
    from app.routes.users import users_bp
    from app.routes.documents import documents_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(documents_bp)

    return app
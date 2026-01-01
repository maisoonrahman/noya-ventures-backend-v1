from flask import Flask
from flask_cors import CORS
from app.models.db import get_db, close_db

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)

    if config_object:
        app.config.from_object(config_object)

    CORS(app)

    app.teardown_appcontext(close_db)

    # Registering minimal blueprints for app to work
    from app.routes.documents import documents_bp
    from app.routes.users import users_bp
    from app.routes.startups import startups_bp
    from app.routes.investors import investors_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(startups_bp)
    app.register_blueprint(investors_bp)

    return app
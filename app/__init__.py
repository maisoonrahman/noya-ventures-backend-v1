from flask import Flask
from flask_cors import CORS
from app.models.db import close_db
from app.config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # loading config
    app.config.from_object(Config)

    CORS(app)

    app.teardown_appcontext(close_db)

    from app.routes.users import users_bp
    from app.routes.documents import documents_bp
    from app.routes.startups import startups_bp
    from app.routes.test import test_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(startups_bp)
    app.register_blueprint(test_bp)

    return app

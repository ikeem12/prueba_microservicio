import os

from flask import Flask

from config import config
from .extensions import db, migrate
from .resources.api_v1 import api_bp

def create_app() -> Flask:

    # initialize the Flask application
    app = Flask(__name__)

    # Load the environment-specific configuration
    env = os.environ.get('APP_SETTINGS', 'development')
    if env not in config:
        raise ValueError(f"Invalid APP_SETTINGS: {env}. Valid options are: {list(config.keys())}")

    # Load the configuration class based on the environment
    cfg_class = config[env]
    app.config.from_object(cfg_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from .models.model import Order

    return app
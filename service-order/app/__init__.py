import os

from flask import Flask

from config import config
from .extensions import db, migrate
from .logger import setup_logging
from .resources.api_v1 import api_bp
from .utils.safe_init import SafeInit
from .utils.exceptions import AppInitializationError, ComponentInitializationError, BlueprintRegistrationError

def create_app() -> Flask:
    """
        Application factory function that creates and configures the Flask app.

        This function sets up the Flask application by:
        - Loading environment-specific configuration.
        - Configuring the logging system.
        - Initializing core components such as the database and migrations.
        - Registering API blueprints.
        - Importing required models for SQLAlchemy registration.

        Returns:
            Flask: A fully configured Flask application instance ready to run.

        Raises:
            AppInitializationError: If any critical step in the setup process fails.
    """
    # initialize the Flask application
    app = Flask(__name__)
    # Set up logging
    app_logger = setup_logging(app)

    # Load the environment-specific configuration
    env = os.environ.get('APP_SETTINGS', 'development')
    if env not in config:
        app_logger.critical("Invalid APP_SETTINGS: %s. Valid options are: %s", env, list(config.keys()))
        raise AppInitializationError(f"Invalid APP_SETTINGS: {env}. Valid options are: {list(config.keys())}")

    # Load the configuration class based on the environment
    cfg_class = config[env]
    app.config.from_object(cfg_class)
    
    try:
        SafeInit(app, init_fn=db.init_app, name='Database')
        SafeInit(app, init_fn=migrate.init_app, name='Migrate')
        app_logger.info("Components initialized successfully.")
    except ComponentInitializationError as cie:
        app_logger.critical("Failed to initialize application components: %s", cie)
        raise 

    try:
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        app_logger.info("API blueprint registered successfully.")
    except Exception as e:
        app_logger.critical("Failed to register API blueprint: %s", e)
        raise BlueprintRegistrationError(f"Failed to register API blueprint: {e}")

    from .models.model import Order

    return app
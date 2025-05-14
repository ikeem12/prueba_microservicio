import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config
from .logger import configure_logging
from .utils.safe_init import SafeInit
from .utils.exceptions import AppInitializationError

# instance global of SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

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
    # create the Flask application
    app = Flask(__name__)

    # configure the logging system
    app_logger = configure_logging(app)

    # Load the environment-specific configuration
    env = os.environ.get('APP_SETTINGS', 'development')
    if env not in config:
        app_logger.critical("Invalid APP_SETTINGS: %s. Valid options are: %s", env, list(config.keys()))
        raise AppInitializationError(f"Invalid APP_SETTINGS: {env}. Valid options are: {list(config.keys())}")

    # configure the application
    cfg_class = config[env]
    app.config.from_object(cfg_class)
    app_logger.info("Flask application configured with %s", cfg_class.__name__)

    try:
        SafeInit(app, init_fn = db.init_app, name="Database", app_logger=app_logger, )
        SafeInit(app, db, init_fn = migrate.init_app, name="Migrations", app_logger=app_logger) 
        app_logger.info("components initialized successfully.")
    except Exception as e:
        app_logger.critical("Failed to initialize components: %s", e, exc_info=True)
        raise AppInitializationError(f"Failed to initialize components: {e}")   

    # Import the model to be registered in SQLAlchemy
    from .models.model import Products

    try:
        # register the api blueprint
        from .resources import create_api_blueprint
        app.register_blueprint(create_api_blueprint(db, app_logger), url_prefix='/api/v1')

        app_logger.info("API blueprint registered with prefix /api/v1")
    except Exception as e:
        app_logger.critical(f"Could not register the API blueprint, aborting startup: {e}", exc_info=True)
        raise AppInitializationError(f"Failed to register blueprint: {e}")

    app_logger.info("Flask application factory setup completed.")

    return app
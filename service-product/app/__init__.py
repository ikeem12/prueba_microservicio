import sys
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config
from .logger import configure_logging
from .utils.safe_init import SafeInit

# instance global of SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """
    Creates and initializes the Flask application.

    This function configures the Flask application, initializes the necessary 
    components such as the database and migrations,configures the Flask system, 
    sets components such as the database and migrations, configures the logging 
    system, registers models and API blueprints.

    Returns:
        Flask: The configured Flask application instance.
    """

    # create the Flask application
    app = Flask(__name__)

    # configure the logging system
    app_logger = configure_logging(app)

    env = os.environ.get('APP_SETTINGS', 'development')
    if env not in config:
        app_logger.critical("Invalid APP_SETTINGS: %s. Valid options are: %s", env, list(config.keys()))
        sys.exit(1)

    cfg_class = config[env]
    # configure the application
    app.config.from_object(cfg_class)
    app_logger.info("Flask application configured with %s", cfg_class.__name__)


    SafeInit(app, init_fn = db.init_app, name="Database", app_logger=app_logger)
    SafeInit(app, db, init_fn = migrate.init_app, name="Migrations", app_logger=app_logger)    

    # Import the model to be registered in SQLAlchemy
    from .models.model import Products

    try:
        # register the api blueprint
        from .resources import create_api_blueprint
        app.register_blueprint(create_api_blueprint(db, app_logger), url_prefix='/api/v1')

        app_logger.info("API blueprint registered with prefix /api/v1")
    except Exception as e:
        app_logger.critical(f"Could not register the API blueprint, aborting startup: {e}", exc_info=True)
        sys.exit(1)

    app_logger.info("Flask application factory setup completed.")

    # Return the configured application instance
    return app
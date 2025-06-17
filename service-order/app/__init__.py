import os

from flask import Flask

from config import config
from .extensions import db, migrate, api, limiter
from .exceptions.internal_exceptions import AppInitializationError, ComponentInitializationError, BlueprintRegistrationError
from .logger import setup_logging
from .resources.api_v1 import api_bp, register_resources
from .repository.repository_order import RepositoryOrder
from .services.ServiceOrder import ServiceOrder
from .utils.initialization_component import InitializationComponent

def create_app() -> Flask:
    """"    
    create and initialize the Flask application with configurations, components, and resources.

    This function follows the factory application pattern. It performs the following steps:
    - Configures logging.
    - Loads the configuration according to the environment defined by the environment variable APP_SETTINGS.
    - Initializes components such as the database and migrations.
    - Registers the API resources and the main blueprint.

    Raises:
        AppInitializationError: If the APP_SETTINGS variable is invalid.
        ComponentInitializationError: If any component (DB, migrations) fails to initialize.
        BlueprintRegistrationError: If an error occurs when registering API endpoints.

    Returns:
        Flask: The fully configured instance of the Flask application.
    """
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
        InitializationComponent(app, init_fn=db.init_app, name='Database')
        InitializationComponent(app, db, init_fn=migrate.init_app, name='Migrate')
        InitializationComponent(app, init_fn=limiter.init_app, name='Limiter')
        app_logger.info("Components initialized successfully.")
    except ComponentInitializationError as cie:
        app_logger.critical("Failed to initialize application components: %s", cie)
        raise 

    from .models.model import Order

    repository = RepositoryOrder(db.session, Order)
    service = ServiceOrder(repository)

    try:
        register_resources(api, service)
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        app_logger.info("API blueprint registered successfully.")
    except Exception as e:
        app_logger.critical("Failed to register API blueprint: %s", e)
        raise BlueprintRegistrationError(f"Failed to register API blueprint: {e}")
    
    return app
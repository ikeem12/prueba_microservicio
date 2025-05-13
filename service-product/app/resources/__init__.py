from logging import Logger

from flask import Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

def create_api_blueprint(db: SQLAlchemy, app_logger:Logger) -> Blueprint:
    """Create the API blueprint for the application.

    This function is used to create and configure the API blueprint, 
    registering the endpoints and configuring the necessary dependencies.

    Nota:
        This function is necessary to avoid circular import problems.
        If the blueprint were registered directly in the application's `__init__.py`,
        a circular import would occur because `db` would not yet be initialized when the blueprint tried to access
        when the blueprint attempted to access it.

    Args:
        db: The database instance.
        app_logger: The main application logger.

    Returns:
        Blueprint: The configured API blueprint.
    """

    # Create a logger especific for the API resources
    resource_logger = app_logger.getChild('resources')
    # Log de inicio del blueprint
    resource_logger.info('Creating API blueprint') 

    # Create the blueprint for the API
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # Import the resources (endpoinst) of the API
    from .resource import EndpointProduct

    # Import the models, services, and repository
    from ..models.model import Products
    from ..services.service import ProductService
    from ..repository.repository import Repository

    # Create the repository and service instances
    repository = Repository(db.session, Products, app_logger)
    product_service = ProductService(repository, app_logger)

    # Register the resources in the API
    api.add_resource(EndpointProduct, '/products', resource_class_kwargs={'product_service': product_service, 'logger': resource_logger})
    resource_logger.info('Resources registered in the API blueprint')


    resource_logger.info('API blueprint created successfully')
    # return the blueprint configured
    return api_bp
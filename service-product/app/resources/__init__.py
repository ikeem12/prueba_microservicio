from flask import Blueprint
from flask_restful import Api

def create_api_blueprint(db):

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # Import the resources
    from .resource import EndpointProduct

    from ..models.model import Products
    from ..services.service import ProductService
    from ..repository.repository import Repository

    repository = Repository(db.session, Products)
    product_service = ProductService(repository)

    api.add_resource(EndpointProduct, '/products', resource_class_args={'product_service': product_service})

    return api_bp
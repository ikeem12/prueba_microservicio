from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Import the resources
from .resource import EndpointCatalog

api.add_resource(EndpointCatalog, '/cakes')
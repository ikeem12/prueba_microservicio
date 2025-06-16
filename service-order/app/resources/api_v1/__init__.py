"""
API blueprint initialization module.

This module defines the `api_bp` blueprint, associates Flask-RESTful with that blueprint,
registers the global error handler and exposes the `register_resources` function
to register API resources related to requests.
"""

from flask import Blueprint
from flask_restful import Api

from ..error_handler import handle_http_exception
from app.extensions import api
from app.services.ServiceOrder import ServiceOrder

api_bp = Blueprint('api', __name__)
api.init_app(api_bp)

# Assign custom error handler for the API
api.handle_error = handle_http_exception

def register_resources(api: Api, service: ServiceOrder) -> None:
    """
    Registers the resources related to requests in the Flask-RESTful API instance.

    This method implements dependency injection, passing the domain service
    (`service`) and validation schemas to each resource as arguments in `resource_class_kwargs`.

    Args:
        api (flask_restful.Api): API instance on which the resources will be registered.
        service (ServiceOrder): Domain service with business logic for orders.
    """
    from .OrderListResource import OrderListResource
    from .OrderDetailResource import OrderDetailResource
    from app.schema.schema_order import SchemaOrderPost, SchemaOrderPut, SchemaOrderId

    api.add_resource(
        OrderListResource, 
        '/orders', 
        resource_class_kwargs={
            'order_service': service, 
            'schema_post': SchemaOrderPost
        }
    )

    api.add_resource(
        OrderDetailResource, 
        '/orders/<int:order_id>', 
        resource_class_kwargs={
            'order_service': service, 
            'schema_put': SchemaOrderPut, 
            'schema_id': SchemaOrderId
            }
    )
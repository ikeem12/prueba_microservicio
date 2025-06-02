from flask import Blueprint

from app.extensions import api, db
from app.utils.error_handler import handle_http_exception
from app.services.ServiceOrder import ServiceOrder
from app.repository.repository_order import RepositoryOrder
from app.models.model import Order
from .OrderListResource import OrderListResource
from .OrderDetailResource import OrderDetailResource

api_bp = Blueprint('api', __name__)
api.init_app(api_bp)

# Register error handler for the API
api.handle_error = handle_http_exception

repository = RepositoryOrder(db.session, Order)
service = ServiceOrder(repository)

api.add_resource(OrderListResource,'/orders', resource_class_kwargs={'order_service': service})
api.add_resource(OrderDetailResource, '/orders/<int:order_id>', resource_class_kwargs={'order_service': service})
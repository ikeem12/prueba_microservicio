from flask import Blueprint

from app.extensions import api
from .OrderResource import OrderResource

api_bp = Blueprint('api', __name__)
api.init_app(api_bp)

api.add_resource(OrderResource,'/orders')
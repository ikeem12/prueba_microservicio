import logging
from typing import Any

from flask_restful import Resource
from flask import request
from pydantic import ValidationError

from ..succes_response import wrap_success_response
from app.exceptions.pydantic_exceptions import PydanticValidationError
from app.schema.schema_order import SchemaOrderPost
from app.services.ServiceOrder import ServiceOrder

logger = logging.getLogger(__name__)

class OrderListResource(Resource):
    """
    RESTful API resource that manages operations on the request collection (GET, POST).

    This class allows:
    - List all existing orders (`GET`).
    - Create a new order (`POST`).

    Attributes:
        order_service: Service that encapsulates the business logic for order management.
        schema_post: Validation schema for the creation of a new order.

    Decorators:
        Each method uses `@wrap_success_response` to standardize the structure of successful responses.
    """

    def __init__(self, order_service: ServiceOrder, schema_post: type[SchemaOrderPost]):
        self.order_service = order_service
        self.schema_post = schema_post

    @wrap_success_response("Orders retrieved successfully")
    def get(self) -> list[dict[str, Any]]:
        try:
            return self.order_service.get_all_order()
        except Exception as e:
            logger.error("Error retrieving orders: %s", e, exc_info=True)
            raise

    @wrap_success_response("Order created successfully")
    def post(self) -> None:
        try:

            order_data = self.schema_post(**request.get_json()).model_dump(exclude_unset=True)
            
            if self.order_service.add_Order(order_data):
                return  None
            
        except ValidationError as e:
            logger.error("Validation error: %s", e.errors())
            raise PydanticValidationError(e)
        
        except Exception as e:
            logger.error("Error creating order: %s", e)
            raise
import logging
from typing import Any

from flask_restful import Resource
from flask import request
from pydantic import ValidationError

from ..succes_response import wrap_success_response
from app.exceptions.pydantic_exceptions import PydanticValidationError
from app.schema.schema_order import SchemaOrderPut, SchemaOrderId
from app.services.ServiceOrder import ServiceOrder

logger = logging.getLogger(__name__)

class OrderDetailResource(Resource):
    """
    RESTful API resource that manages operations on a specific request (GET, PUT, DELETE).

    This class allows to:
    - Get details of an order by its ID (`GET`).
    - Update an existing order (`PUT`).
    - Delete an order (`DELETE`).

    Attributes:
        order_service: Service that encapsulates the business logic for orders.
        schema_put: Validation scheme for order update data.
        schema_id: Validation scheme for the `order_id` parameter.

    Decorators:
        Each method uses `@wrap_success_response` to standardize the success response.
    """
    def __init__(self, order_service: ServiceOrder, schema_put: type[SchemaOrderPut], schema_id: type[SchemaOrderId]):
        self.order_service = order_service
        self.schema_put = schema_put
        self.schema_id = schema_id

    @wrap_success_response("Order retrieved successfully")
    def get(self, order_id: int) -> dict[str, Any]:
        try:
            id_validated = self.schema_id(order_id=order_id)
            return self.order_service.get_order(id_validated.order_id)
        
        except ValidationError as e:
            logger.error("Validation error: %s", e.errors())
            raise PydanticValidationError(e)
        
        except Exception as e:
            logger.error("Handled API error: %s", e)
            raise

    @wrap_success_response("Order update successfully")
    def put(self, order_id: int) -> None:
        try:
            id_validated = self.schema_id(order_id=order_id)
            order_data = self.schema_put(**request.get_json()).model_dump(exclude_unset=True)
            if self.order_service.update_order(id_validated.order_id, order_data):
                return None
            
        except ValidationError as e:
            logger.error("Validation error: %s", e.errors())
            raise PydanticValidationError(e)
        
        except Exception as e:
            logger.error("Handled API error: %s", e, exc_info=True)
            raise

    @wrap_success_response("Order eliminated successfully")
    def delete(self, order_id: int) -> None:
        try:
            id_validated = self.schema_id(order_id=order_id)
            if self.order_service.delete_order(id_validated.order_id):
                return None
            
        except ValidationError as e:
            logger.error("Validation error: %s", e.errors())
            raise PydanticValidationError(e)
        
        except Exception as e:
            logger.error("Handled API error: %s", e, exc_info=True)
            raise
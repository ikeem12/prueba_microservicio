from datetime import date
from typing import Any

from app.interfaces.interfaces_services import IOrderService
from app.repository.repository_order import RepositoryOrder
from app.exceptions.api_exceptions import BadRequestError
from app.utils.utils import str_to_object_date

class ServiceOrder(IOrderService):
    """
    Service layer implementation for managing Order operations.

    This class acts as an intermediary between the application logic and the repository layer, 
    applying business rules before delegating data access to the repository.

    Responsibilities:
    - Retrieve all orders or a specific order.
    - Validate and create new orders.
    - Validate and update existing orders.
    - Delete orders.

    Attributes:
        order_repository: Repository instance responsible for data access operations related to orders.

    Business Rules:
    - Delivery date must not be earlier than today's date when creating an order.
    - Orders with status "delivered" or "cancelled" cannot be updated.
    """
    def __init__(self, order_repository: RepositoryOrder):
        self.order_repository = order_repository

    def get_all_order(self) ->  list[dict[str, Any]]:
        return self.order_repository.get_all_orders()

    def get_order(self, order_id: int) -> dict[str, Any]:
        return self.order_repository.get_order(order_id)
    
    def add_Order(self, order_data: dict[str, Any]) -> bool:
        
        order_data["delivery_date"] = str_to_object_date(order_data["delivery_date"])

        if "delivery_date" in order_data and order_data["delivery_date"] < date.today():
            raise BadRequestError("Delivery date cannot be earlier than order date.")
        return self.order_repository.add_Order(order_data)

    def update_order(self, order_id: int, order_data: dict[str, Any]) -> bool:
        order = self.order_repository.get_order(order_id)
        if order["status"] in ["delivered", "cancelled"]:
            raise BadRequestError("A delivered or cancelled order cannot be modified.")
        return self.order_repository.update_order(order_id, order_data)

    def delete_order(self, order_id: int) -> bool:
        return self.order_repository.delete_order(order_id)
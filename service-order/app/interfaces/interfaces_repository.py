from abc import ABC, abstractmethod
from typing import Any

class IReadRepository(ABC):
    """
    Interface for read-only operations on the Order repository.

    Defines the contract for retrieving order data from the persistence layer.
    """
    @abstractmethod
    def get_all_orders(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> dict[str, Any]:
        pass

class IWriteRepository(ABC):
    """
    Interface for write operations on the Order repository.

    Defines the contract for creating and updating orders in the persistence layer.
    """
    @abstractmethod
    def add_Order(self, order_data:  dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def update_order(self, order_id: int, order_data: dict[str, Any]) -> bool:
        pass

class IDeleteRepository(ABC):
    """
    Interface for delete operations on the Order repository.

    Defines the contract for removing orders from the persistence layer.
    """
    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        pass

class IOrderRepository(IReadRepository, IWriteRepository, IDeleteRepository):
    """
    Aggregated interface for full CRUD operations on orders.

    Inherits read, write, and delete capabilities to define the complete contract
    for interacting with Order entities in the persistence layer.
    """
    pass
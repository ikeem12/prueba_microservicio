from abc import ABC, abstractmethod
from typing import Any

class IReadOrder(ABC):
    """
    Interface for read-only operations on the Order repository.

    Defines the contract for retrieving order data from the persistence layer.
    """
    @abstractmethod
    def get_all_order(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> dict[str, Any]:
        pass

class IWriteOrder(ABC):
    """
    Interface for write operations on the Order repository.

    Defines the contract for creating and updating order data in the persistence layer.
    """
    @abstractmethod
    def add_Order(self, order_data:  dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def update_order(self, order_id: int, order_data: dict[str, Any]) -> bool:
        pass

class IDeleteOrder(ABC):
    """
    Interface for delete operations on the Order repository.

    Defines the contract for removing order data from the persistence layer.
    """
    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        pass

class IOrderService(IReadOrder, IWriteOrder, IDeleteOrder):
    """
    Interface for full CRUD operations on the Order repository.

    Combines read, write, and delete interfaces to define the complete contract 
    for managing orders in the service layer.
    """
    pass
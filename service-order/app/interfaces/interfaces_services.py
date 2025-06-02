from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IReadOrder(ABC):
    @abstractmethod
    def get_all_order(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Dict[str, Any]:
        pass

class IWriteOrder(ABC):
    @abstractmethod
    def add_Order(self, order_data:  Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> bool:
        pass

class IDeleteOrder(ABC):
    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        pass

class IOrderService(IReadOrder, IWriteOrder, IDeleteOrder):
    pass
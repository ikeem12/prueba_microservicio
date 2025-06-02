from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IReadRepository(ABC):
    @abstractmethod
    def get_all_orders(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Dict[str, Any]:
        pass

class IWriteRepository(ABC):
    @abstractmethod
    def add_Order(self, order_data:  Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> bool:
        pass

class IDeleteRepository(ABC):
    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        pass

class IOrderRepository(IReadRepository, IWriteRepository, IDeleteRepository):
    pass
from abc import ABC, abstractmethod
from typing import List, Dict

class IReadProduct(ABC):
    @abstractmethod
    def get_product(self, offset: int, limit: int) -> List:
        pass

class IWriteProduct(ABC):
    @abstractmethod
    def add_product(self, cake_data: Dict) -> bool:
        pass

    @abstractmethod
    def update_product(self, cake_id: int, cake_data: Dict) -> bool:
        pass

class IDeleteProduct(ABC):
    @abstractmethod
    def delete_product(self, cake_id: int) -> bool:
        pass

class IProductService(IReadProduct, IWriteProduct, IDeleteProduct):
    pass
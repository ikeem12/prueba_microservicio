from ..interfaces.interfaces import IProductService
from ..repository.repository import Repository

class ProductService(IProductService):
    def __init__(self, repository: Repository):
        self.repository = repository

    def get_product(self, offset, limit):
        products = self.repository.get(offset, limit)

        return [dict(product) for product in products]
    
    def add_product(self, product_data: dict[str]) -> bool:
        return self.repository.add(product_data)
    
    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)
    
    def update_product(self, product_id: int, product_data: dict[str]) -> bool:
        pass

from logging import Logger
from typing import Dict, List, Any

from ..interfaces.interface_service import IProductService
from ..repository.repository import Repository

class ProductService(IProductService):
    """"Service class for managing products."""

    def __init__(self, repository: Repository, logger: Logger):
        self.repository = repository
        self.logger = logger.getChild('ProductService') 

    def get_product(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """Get products from the repository with pagination.

        Args:
            offset (int): The starting point for pagination.
            limit (int): The number of products to retrieve.

        Returns:
            list[Dict[str,T]]: A list of items fetched from the database.
        """
        try:
            products = self.repository.get(offset, limit)
            self.logger.debug("Fetching products with offset=%s and limit=%s", offset, limit)
            
            results = [dict(product) for product in products]

            self.logger.debug("Transformed %s products into dictionaries", len(results))
        
            return  results
        except Exception as e:
            self.logger.error("Error fetching products: %s", e, exc_info=True)
            raise

    def add_product(self, cake_data):
        pass

    def update_product(self, cake_id, cake_data):
        pass

    def delete_product(self, cake_id):
        pass
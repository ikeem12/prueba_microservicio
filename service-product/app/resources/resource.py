from logging import Logger
from typing import Dict, List, Any

from flask_restful import Resource, reqparse
from flask import jsonify

from ..interfaces.interface_service import IProductService

class EndpointProduct(Resource):
    """
    Endpoint for managing products.

    This endpoint provides operations for managing products, such as retrieving
    a list of products with pagination.

    Available HTTP methods:
        - GET: Retrieve a list of products with pagination.

    Args:
        product_service (IProductService): The service for managing products.
        logger (Logger): The logger for logging messages.
    """

    def __init__(self, product_service: IProductService, logger: Logger):
        self.product_service = product_service
        self.logger = logger

    def get(self) -> List[Dict[str, Any]]:
        """Get a list of products with pagination."""
        self.logger.info("GET /products request received")

        # Define the request parser for pagination
        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int,  default=0,  location='args', help='Offset for pagination')
        parser.add_argument('limit', type=int, default=10,  location='args' ,help='Number of items to return')
        args = parser.parse_args()

        # Get the offset and limit from the parsed arguments
        offset = args['offset']
        limit = args['limit']

        self.logger.info("GET /products - Pagination parameters: offset=%s, limit=%s", offset, limit)

        try:
            # Fetch products from the service 
            products = self.product_service.get_product(offset, limit)
            self.logger.info("GET /products - Found %s products", len(products))
            return jsonify(products)
        except Exception as e:
            self.logger.error("GET /products - Error: %s", str(e), exc_info=True)
            return jsonify({"error": "An error occurred while fetching products."})
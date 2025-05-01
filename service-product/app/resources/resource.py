from flask_restful import Resource, reqparse

class EndpointProduct(Resource):

    def __init__(self, product_service):
        self.product_service = product_service

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int,  default=0,  location='args', help='Offset for pagination')
        parser.add_argument('limit', type=int, default=10,  location='args' ,help='Number of items to return')
        args = parser.parse_args()

        offset = args['offset']
        limit = args['limit']


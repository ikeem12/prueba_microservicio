class APIError(Exception):
    def __init__(self, message="An error occurred", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class OrderNotFoundError(APIError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class BadRequestError(APIError):
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)
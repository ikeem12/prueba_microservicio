class APIError(Exception):
    """
    Base class for custom application-specific API exceptions.

    Attributes:
        message (str): A human-readable error message.
        status_code (int): The HTTP status code associated with the error.
    """
    def __init__(self, message="An error occurred", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class OrderNotFoundError(APIError):
    """
    Exception raised when a requested order is not found.

    Inherits from APIError and sets a default HTTP status code of 404.
    """
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class BadRequestError(APIError):
    """
    Exception raised for bad or invalid API requests.

    Inherits from APIError and sets a default HTTP status code of 400.
    """
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)
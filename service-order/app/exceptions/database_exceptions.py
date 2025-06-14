class DatabaseError(Exception):
    """
    Base class for exceptions related to database operations.

    Attributes:
        message (str): A human-readable description of the error.
        status_code (int): HTTP status code associated with database errors (default is 500).
    """
    def __init__(self, message="Database error"):
        self.message = message
        self.status_code = 500
        super().__init__(message)

class ConnectionError(DatabaseError):
    """
    Exception raised when the application fails to connect to the database.

    Inherits from DatabaseError and sets a default error message.
    """
    def __init__(self, message="Database connection failed"):
        super().__init__(message)

class QueryError(DatabaseError):
    """
    Exception raised when a database query fails to execute properly.

    Inherits from DatabaseError and sets a default error message.
    """
    def __init__(self, message="Database query failed"):
        super().__init__(message)   
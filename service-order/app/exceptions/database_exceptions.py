class DatabaseError(Exception):
    def __init__(self, message="Database error"):
        self.message = message
        self.status_code = 500
        super().__init__(message)

class ConnectionError(DatabaseError):
    def __init__(self, message="Database connection failed"):
        super().__init__(message)

class QueryError(DatabaseError):
    def __init__(self, message="Database query failed"):
        super().__init__(message)   
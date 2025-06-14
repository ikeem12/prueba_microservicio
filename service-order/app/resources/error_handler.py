from flask import jsonify, make_response
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException

from app.exceptions.api_exceptions import APIError
from app.exceptions.database_exceptions import DatabaseError
from app.exceptions.pydantic_exceptions import PydanticValidationError

def handle_http_exception(e: Exception) -> Response:
    """
    Global error handler for HTTP and custom application exceptions.

    This function captures and handles different types of exceptions raised during API execution, 
    including:
    - `PydanticValidationError`: returns validation details and a status code.
    - `HTTPException` (from Werkzeug): returns the associated HTTP status code and description.
    - Custom exceptions like `APIError` and `DatabaseError`: return predefined messages and status codes.

    If the exception is not recognized, it falls back to a generic 500 Internal Server Error response.

    Args:
        e (Exception): The exception instance raised during request processing.

    Returns:
        Response: A Flask Response object containing a standardized JSON error structure.
    """

    if isinstance(e, PydanticValidationError):
        return make_response(jsonify({
            "status": "error",
            "message": e.message,
            "errors": e.details,
            "status_code": e.status_code
        }), e.status_code)

    exception_handlers = {
        HTTPException: lambda err: (err.code, err.description),
        APIError: lambda err: (err.status_code, err.message),
        DatabaseError: lambda err: (err.status_code, err.message),
    }

    for exc_type, handler in exception_handlers.items():
        if isinstance(e, exc_type):
            status_code, message = handler(e)
            response = {
                "status": "error",
                "message": message,
                "status_code": status_code
            }
            return make_response(jsonify(response), status_code)

    # Fallback for unexpected exceptions
    return make_response(jsonify({
        "status": "error",
        "message": "Internal server error",
        "status_code": 500
    }), 500)

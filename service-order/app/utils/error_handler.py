from flask import jsonify, make_response
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException

from app.exceptions.api_exceptions import APIError
from app.exceptions.database_exceptions import DatabaseError

def handle_http_exception(e: Exception) -> Response:
    """"
        Global error handler for HTTP and application-specific exceptions.
    """

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

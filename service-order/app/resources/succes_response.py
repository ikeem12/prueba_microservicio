from functools import wraps
import logging
from typing import Callable, ParamSpec

from flask import jsonify, make_response, Response

logger = logging.getLogger(__name__)

P = ParamSpec("P")

def wrap_success_response(message: str, status_code: int = 200) -> Callable[[Callable[P, object]], Callable[P, Response]]:
    """
    Decorator that wraps a Flask view function to standardize 
    the JSON response on success.

    It also logs a success message in the application log.

    Args:
        message (str): Success message to be included in the response.
        status_code (int, optional): HTTP status code to return. Default is 200.

    Returns:
        Callable: Decorator function that wraps the original function and returns 
        a standard JSON response with the data produced by that function.
    """
    def decorator(func: Callable[P, object]) -> Callable[P, Response]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Response:
            result = func(*args, **kwargs)
            logger.info("Success: %s | Status: %d", message, status_code)
            response = jsonify({
                "status": "success",
                "message": message,
                "data": result if result is not None else {},
                "status_code": status_code
            })
            return make_response(response, status_code)
        return wrapper
    return decorator
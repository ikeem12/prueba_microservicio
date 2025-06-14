from pydantic import ValidationError

class PydanticValidationError(Exception):
    """
    Exception raised when a Pydantic model fails validation.

    Attributes:
        message (str): A generic error message indicating validation failure.
        details (List[Dict[str, str]]): A list of detailed validation errors, including:
            - 'campo': the path to the invalid field.
            - 'mensaje': the corresponding validation error message.
        status_code (int): HTTP status code to return (default is 422).
    """
    def __init__(self, error: ValidationError, status_code: int = 422):
        self.message = "Validation failed"
        self.details = [
            {
                "campo": " -> ".join(map(str, err["loc"])),
                "mensaje": err["msg"]
            }
            for err in error.errors()
        ]
        self.status_code = status_code
        super().__init__(self.message)
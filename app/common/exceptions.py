class Error(Exception):
    """Base class for exceptions in this project."""
    pass


class ValidationError(Error):
    """Exception raised when data sent by client is invalid."""

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


class JsonValidationError(ValidationError):
    """Exception raised when JSON data send by client is invalid."""
    pass

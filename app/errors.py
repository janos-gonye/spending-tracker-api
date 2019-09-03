from app.common import js
from app.common.exceptions import JsonValidationError, ValidationError


def init_app(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return e.message, e.status_code

    @app.errorhandler(JsonValidationError)
    def handle_json_validation_error(e):
        return js(e.message, e.status_code)

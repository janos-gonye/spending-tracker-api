from app.common import js
from app.common.exceptions import ValidationError


def init_app(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return e.message, e.status_code

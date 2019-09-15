from functools import wraps

from flask import request

from app.common.exceptions import ValidationError


def json_validator_template(validator=None):
    def decorator(f):

        @wraps(f)
        def decorated(**kwargs):
            data = request.get_json()
            if not data:
                raise ValidationError('JSON payload required.')
            if validator:
                validator(data, **kwargs)
            return f(data, **kwargs)
        return decorated
    return decorator
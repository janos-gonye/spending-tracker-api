from time import time
from functools import wraps

from flask import request

from app.common.exceptions import ValidationError
from app.common.token import decode_token


def json_validator_template(validator=None):
    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json()
            if not data:
                raise ValidationError('JSON payload required.')
            if validator:
                validator(data, *args, **kwargs)
            return f(data, *args, **kwargs)
        return decorated
    return decorator


def token_as_arg_validator_template(validator=None):
    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                raise ValidationError('Token missing.')
            payload = decode_token(token)
            if not payload:
                raise ValidationError('Token invalid.')
            expires_at = payload.get('expiresAt')
            if expires_at and float(expires_at) < time():
                raise ValidationError('Token expired.', 401)
            return f(payload, *args, **kwargs)
        return decorated
    return decorator

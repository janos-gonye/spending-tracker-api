from functools import wraps

from app.common import js
from app.common.exceptions import JsonValidationError, ValidationError


def jsonify_view(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
        except ValidationError as err:
            raise JsonValidationError(err.message, err.status_code)
        length = len(res)
        kwargs = {}
        if length == 2:
            msg, status_code = res
        if length == 3:
            msg, status_code, kwargs = res
        else:
            msg, status_code = res, 200
        return js(msg, status_code, **kwargs)
    return decorated


def require_json_validator(f):

    @wraps(f)
    def decorated(data, *args, **kwargs):
        if not data:
            raise ValidationError('JSON payload required.')
        return f(data, *args, **kwargs)
    return decorated

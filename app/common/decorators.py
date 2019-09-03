from functools import wraps

from app.common import js
from app.common.exceptions import ValidationError


def jsonify_view(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        res = f(*args, **kwargs)
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
    def decorated(*args, **kwargs):
        if not kwargs.get('data'):
            raise ValidationError('JSON payload required.')
        return f(*args, **kwargs)
    return decorated

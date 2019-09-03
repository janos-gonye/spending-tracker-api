from functools import wraps

from app.common import js
from app.common.exceptions import ValidationError


def jsonify_view(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        res = f(*args, **kwargs)
        l = len(res)
        if l == 2:
            msg, status_code = res
            return js(msg, status_code)
        if l == 3:
            msg, status_code, kwargs = res
            return js(msg, status_code, **kwargs)        
        return js(msg, status_code)
    return decorated


def require_json_validator(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if not kwargs.get('data'):
            raise ValidationError('JSON payload required.')
        return f(*args, **kwargs)
    return decorated

from functools import wraps

from app.common import js


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

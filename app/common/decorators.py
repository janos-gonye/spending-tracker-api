from functools import wraps

from app.common import js


def jsonify_view(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        msg, status_code = f(*args, **kwargs)
        return js(msg, status_code)
    return decorated

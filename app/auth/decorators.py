from functools import wraps, partial
from time import time

from flask import request

from app.auth.models import User
from app.utils import js
from app.utils.token import decode_token


def token_required(f=None, min_role=10):
    """
    checking token and permission
    --
    use as the followings
    login_required
    login_required(min_role=50) <-- this is what partial *magic* is for
    """
    if not f:
        return partial(token_required, min_role=min_role)

    @wraps(f)
    def decorated(*args, **kwargs):
        # Authorization: Bearer <token>

        token = request.headers.get('Authorization')

        if not token:
            return js('Token missing.', 401)

        token = token[7:]  # cut of <Bearer >

        payload = decode_token(token)
        if not payload:
            return js('Invalid token.', 401)

        current_user = User.query.filter_by(
            public_id=payload.get('public_id')).first()

        if payload.get('expiresAt') and payload['expiresAt'] < time():
            return js('Session expired.', 401, expired=True)
        if current_user:
            if int(current_user.role) >= min_role:
                return f(current_user, *args, **kwargs)
            return js('Permission denied.', 403)

        return js('Invalid token.', 401)

    return decorated

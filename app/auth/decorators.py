from functools import partial, wraps
from time import time

from flask import request

from app.auth.models import User
from app.common.token import decode_token, TokenTypes


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
            return 'Token missing.', 401

        token = token[7:]  # chop off <Bearer >
        payload = decode_token(token, TokenTypes.ACCESS)
        if not payload:
            return 'Invalid token.', 401

        current_user = User.query.filter_by(
            public_id=payload.get('public_id')).first()

        if payload.get('expiresAt') and payload['expiresAt'] < time():
            # TODO: Do something with expired.
            return 'Session expired.', 401, {"expired": True}
        if current_user:
            if int(current_user.role) >= min_role:
                return f(current_user, *args, **kwargs)
            return 'Permission denied.', 403

        return 'Invalid token.', 401

    return decorated

from time import time
from uuid import uuid4

from flask import current_app as app
from jwt import decode, encode
from jwt.exceptions import PyJWTError  # base class of all pyjwt exceptions


class TokenTypes:
    REGISTRATION = 0
    CANCEL_REGISTRATION = 1
    ACCESS = 2
    REFRESH = 3
    FORGOT_PASSWORD = 4


# Warning, default arguments are evaluated at definition time
# therefore never type e.g.: from_=time() in a function's definition
def encode_token(payload, token_type, lifetime=3600, from_=None):
    """
    <lifetime> as seconds
    if lifetime is None, the token never expires --> ! Not recommended
    ---
    <from_> as seconds since epoch
    if from_ is None, set from_ to the current timestamp
    """
    if not from_:
        from_ = time()

    if payload.get('expiresAt'):
        raise Exception(
            "Programming Error: 'Payload' dict already has key 'expiresAt'")

    if lifetime:
        payload['expiresAt'] = from_ + lifetime
    else:
        # add some randomness, even if token never expires
        # otherwise same user, same password input would cause same output
        payload['randomness'] = str(uuid4())
    payload[token_type] = True

    return encode(payload, str(app.secret_key))


def decode_token(token, token_type):
    """
    if token invalid, return None
    """

    if type(token) is bytes:
        token = token.decode('utf-8')

    try:
        payload = decode(token, app.secret_key)
    except PyJWTError:
        return None
    if payload.get(token_type) is not True:
        return None

    return payload

from time import time
from uuid import uuid4

from flask import current_app as app

from jwt import encode, decode
from jwt.exceptions import PyJWTError  # base class of all pyjwt exceptions


# Big Warning, default arguments are evaluated at definition time
# therefore never type e.g.: from_=time() in a function's definition
def encode_token(payload, lifetime=3600, from_=None):
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
        raise Error(
            "Programming Error: 'Payload' dict already has key 'expiresAt'")

    if lifetime:
        payload['expiresAt'] = from_ + lifetime
    else:
        # add some randomness, even if token never expires
        # otherwise same user, same password input would cause same output
        payload['randomness'] = str(uuid4())

    return encode(payload, str(app.secret_key))


def decode_token(token):
    """
    if token invalid, return None
    """

    if type(token) is bytes:
        token = token.decode('utf-8')

    try:
        payload = decode(token, app.secret_key)
    except PyJWTError as err:
        return None

    return payload

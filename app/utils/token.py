from flask import current_app as app

from jwt import encode, decode
from jwt.exceptions import PyJWTError # base class of all pyjwt exceptions
from time import time


def encode_token(payload, lifetime=3600, from_=time()):
	"""
	<lifetime> in seconds
			   if lifetime is None, the token never expires --> ! Not recommended
	---
	<from_> in seconds, default value: the moment the functions is called
	"""
	if payload.get('expiresAt'):
		raise Error("Programming Error: 'Payload' dict already has key 'expiresAt'")

	if lifetime:
		payload['expiresAt'] = from_ + lifetime

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

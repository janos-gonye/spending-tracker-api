from flask import current_app as app

from time import time
from jwt import encode


def gen_token(payload, lifetime=3600, from_=time()):
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

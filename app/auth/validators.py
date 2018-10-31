from time import time

from app.auth.models import User
from app.utils import js
from app.utils.validators import validate_email, validate_password


def validate_registration_data(data):
	"""doesn't check if user already registered"""
	if not data:
		return js('JSON payload missing.', 400)

	email = data.get('email')
	password = data.get('password')

	if not email and not password:
		return js('Email and password missing.', 400)

	if not email:
		return js('Email missing.', 400)

	if not password:
		return js('Password missing.', 400)

	if not validate_email(email):
		return js('Invalid email address.', 400)

	if not validate_password:
		return js('Password\'s length must be at least 6 characters. Must contain number, upper and lower case latters.', 400)

	return js('Email and password are valid.')


def validate_confirm_registration_data(data):
	"""doesn't check if user already registered"""

	json, status_code = validate_registration_data(data=data)

	if status_code != 200:
		return js('Token invalid.', 400)

	expiresAt = data.get('expiresAt')
	if expiresAt and int(expiresAt) < time():
		return js('Token expired.', 400)

	return js('Token valid.')


def already_registered(email):
	return bool(User.query.filter_by(email=email).first())

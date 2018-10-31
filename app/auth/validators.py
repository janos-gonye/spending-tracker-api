from time import time

from werkzeug.security import generate_password_hash

from app.auth.models import User
from app.utils import js, succ_status
from app.utils.validators import validate_email, validate_password


def validate_registration_data(data):
	"""doesn't check if user already registered"""
	if not data:
		return js('Only JSON payload accepted.', 400)

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

	if not validate_password(password):
		return js('Password\'s length must be at least 6 characters. Must contain number, upper and lower case latters.', 400)

	if email and already_registered(email=email):
		return js('Email address already registered.', 400)

	return js('Email and password are valid.', 201)


def validate_confirm_registration_data(data):
	"""doesn't check if user already registered"""

	json, status_code = validate_registration_data(data=data)

	if not succ_status(code=status_code) != 200:
		return js('Token invalid.', 400)

	if already_registered(email=data['email']):
		return js('Registration already confirmed.', 400) # this time with a different message

	expiresAt = data.get('expiresAt')
	if expiresAt and int(expiresAt) < time():
		return js('Token expired.', 400)

	return js('Token valid.')


def already_registered(email):
	return bool(User.query.filter_by(email=email).first())


def validate_login(data):
	if not data:
		return js('Only JSON payload accepted.', 400)

	email = data.get('email')
	password = data.get('password')

	if not email or not password:
		return js('Invalid credentials.', 401)

	user = User.query.filter_by(email=email).first()

	if not user or not user.check_password(password):
		return js('Invalid credentials.', 401)

	return js('Valid credentials.', 201)

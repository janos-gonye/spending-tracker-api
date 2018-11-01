from time import time

from app.auth.models import User
from app.utils import succ_status
from app.utils.validators import validate_email, validate_password


def validate_registration_data(data):
	"""doesn't check if user already registered"""
	if not data:
		return 'Only JSON payload accepted.', 400

	email = data.get('email')
	password = data.get('password')

	if not email and not password:
		return 'Email and password missing.', 400

	if not email:
		return 'Email missing.', 400

	if not password:
		return 'Password missing.', 400

	if not validate_email(email):
		return 'Invalid email address.', 400

	if not validate_password(password):
		return 'Password\'s length must be at least 6 characters. Must contain number, upper and lower case letters.', 400

	if email and already_registered(email=email):
		return 'Email address already registered.', 400

	return 'Email and password are valid.', 201


def validate_confirm_registration_data(data):
	"""doesn't check if user already registered"""

	_, status_code = validate_registration_data(data=data)

	if not succ_status(code=status_code):
		return 'Token invalid.', 400

	if already_registered(email=data['email']):
		return 'Registration already confirmed.', 400 # this time with a different message

	expiresAt = data.get('expiresAt')
	if expiresAt and float(expiresAt) < time():
		return 'Token expired.', 400

	return 'Token valid.', 200


def already_registered(email):
	return bool(User.query.filter_by(email=email).first())


def validate_login(data):
	if not data:
		return 'Only JSON payload accepted.', 400

	email = data.get('email')
	password = data.get('password')

	if not email or not password:
		return 'Invalid credentials.', 401

	user = User.query.filter_by(email=email).first()

	if not user or not user.check_password(password):
		return 'Invalid credentials.', 401

	return 'Valid credentials.', 201

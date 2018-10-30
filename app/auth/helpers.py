from time import time

from flask import jsonify

from app.utils.validators import validate_email, validate_password
from app.auth.models import User


def validate_registration_data(data):
	"""doesn't check if user already registered"""
	if not data:
		return jsonify({'message': 'JSON payload missing.'}), 400

	email = data.get('email')
	password = data.get('password')

	if not email and not password:
		return jsonify({'message': 'Email and password missing.'}), 400

	if not email:
		return jsonify({'message': 'Email missing.'}), 400

	if not password:
		return jsonify({'message': 'Password missing.'}), 400

	if not validate_email(email):
		return jsonify({'message': 'Invalid email address.'}), 400

	if not validate_password:
		return jsonify({'message': 'Password\'s length must be at least 6 characters. Must contain number, upper and lower case latters.'})

	return jsonify({'message': 'Email and password are valid.'}), 200


def validate_confirm_registration_data(data):
	"""doesn't check if user already registered"""

	json, status_code = validate_registration_data(data=data)

	if status_code != 200:
		return jsonify({'message': 'Token invalid.'}), 400

	expiresAt = data.get('expiresAt')
	if expiresAt and int(expiresAt) < time():
		return jsonify({'Token expired.'}), 400

	return jsonify({'message': 'Token valid.'}), 200


def already_registered(email):
	return bool(User.query.filter_by(email=email).first())

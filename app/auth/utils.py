from flask import jsonify

from app.utils.validators import validate_email, validate_password
from app.auth.models import User


def validate_registration_data(data):

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

	if User.query.filter_by(email=email).first():
		return jsonify({'message': 'Email address already registered.'}), 400

	return jsonify({'message': 'Email and password are valid.'}), 200

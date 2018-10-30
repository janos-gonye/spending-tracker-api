from uuid import uuid4
# Use uuid4 bacause uuid1() may compromise privacy since it creates a UUID
# containing the computer’s network address. uuid4() creates a random UUID.

from flask import jsonify, request, current_app as app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app.auth import auth
from app.auth.helpers import already_registered
from app.auth.helpers import validate_registration_data
from app.auth.helpers import validate_confirm_registration_data
from app.auth.mail import send_reg_confirm_mail
from app.auth.mail import send_reg_confirmed_mail
from app.auth.models import User
from app.db import db
from app.utils.token import encode_token, decode_token


@auth.route('/registration', methods=['POST'])
def registration():
	data = request.get_json()

	json, status_code = validate_registration_data(data=data)

	if status_code != 200:
		return json, status_code

	if already_registered(email=data['email']):
		return jsonify({'message': 'Email address already registered.'}), 400

	payload = {'email': data['email'], 'password': data['password']}
	token = encode_token(payload=payload, lifetime=app.config['REGISTRATION_TOKEN_LIFETIME'])

	send_reg_confirm_mail(recipient=data['email'], token=token.decode('utf-8'))

	return jsonify({'message': 'Confirmation email has been sent.'}), 200


@auth.route('/registration/confirm', methods=['GET'])
def confirm_registration():
	token = request.args.get('token')

	if not token:
		return jsonify({'message': 'Token missing.'}), 400

	data = decode_token(token)	
	json, status_code = validate_confirm_registration_data(data=data)

	if status_code != 200:
		return json, status_code

	if already_registered(email=data['email']):
		return jsonify({'message': 'Registration already confirmed.'}), 400

	new_user = User(public_id=uuid4(), email=data['email'], password=data['password'])
	
	try:
		db.session.add(new_user)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return jsonify({'message': 'Internal Server Error'}), 500

	send_reg_confirmed_mail(recipient=data['email'])

	return jsonify({'message': 'Registration confirmed.'}), 200


@auth.route('/registration', methods=['DELETE'])
def delete_registration():
	pass


@auth.route('/login', methods=['POST'])
def login():
	pass

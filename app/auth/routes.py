from uuid import uuid4
# Use uuid4 bacause uuid1() may compromise privacy since it creates a UUID
# containing the computer’s network address. uuid4() creates a random UUID.

from flask import request, current_app as app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app.auth import auth
from app.auth.validators import already_registered
from app.auth.validators import validate_registration_data
from app.auth.validators import validate_confirm_registration_data
from app.auth.mail import send_reg_confirm_mail
from app.auth.mail import send_reg_confirmed_mail
from app.auth.models import User
from app.db import db
from app.utils import js 
from app.utils.token import encode_token, decode_token


@auth.route('/registration', methods=['POST'])
def registration():
	data = request.get_json()

	json, status_code = validate_registration_data(data=data)

	if status_code != 200:
		return json, status_code

	if already_registered(email=data['email']):
		return js('Email address already registered.', 400)

	payload = {'email': data['email'], 'password': data['password']}
	token = encode_token(payload=payload, lifetime=app.config['REGISTRATION_TOKEN_LIFETIME'])

	send_reg_confirm_mail(recipient=data['email'], token=token.decode('utf-8'))

	return js('Confirmation email has been sent.', 200)


@auth.route('/registration/confirm', methods=['GET'])
def confirm_registration():
	token = request.args.get('token')

	if not token:
		return js('Token missing.', 400)

	data = decode_token(token)	
	json, status_code = validate_confirm_registration_data(data=data)

	if status_code != 200:
		return json, status_code

	if already_registered(email=data['email']):
		return js('Registration already confirmed.', 400)

	new_user = User(public_id=uuid4(), email=data['email'], password=data['password'])
	
	try:
		db.session.add(new_user)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return js('Internal Server Error', 500)

	send_reg_confirmed_mail(recipient=data['email'])

	return js('Registration confirmed.', 200)


@auth.route('/registration', methods=['DELETE'])
def del_registration():
	pass


@auth.route('/registration/confirm', methods=['GET'])
def del_registration_confirm():
	pass


@auth.route('/login', methods=['POST'])
def login():
	pass

@auth.route('/logout', methods=['POST'])
def logout():
	"""blacklist token"""
	pass

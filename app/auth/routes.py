from uuid import uuid4
# Use uuid4 bacause uuid1() may compromise privacy since it creates a UUID
# containing the computer’s network address. uuid4() creates a random UUID.
from time import time

from flask import jsonify, request, current_app as app
from sqlalchemy.exc import SQLAlchemyError

from app.auth import auth
from app.auth.decorators import token_required
from app.auth.mail import send_reg_confirm_mail
from app.auth.mail import send_reg_confirmed_mail
from app.auth.mail import send_cancel_reg_confirm_email
from app.auth.mail import send_cancel_reg_confirmed_email
from app.auth.models import User
from app.auth.validators import validate_confirm_registration_data
from app.auth.validators import validate_login
from app.auth.validators import validate_registration_data
from app.db import db
from app.utils import js, succ_status
from app.utils.token import encode_token, decode_token


@auth.after_request
def no_cache(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "0"
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response


@auth.route('/registration', methods=['POST'])
def registration():
	data = request.get_json()

	message, status_code = validate_registration_data(data=data)

	if not succ_status(code=status_code):
		return js(message, status_code)

	payload = {'email': data['email'], 'password': data['password']}
	token = encode_token(payload=payload, lifetime=app.config['REGISTRATION_TOKEN_LIFETIME'])

	send_reg_confirm_mail(recipient=data['email'], token=token.decode('utf-8'))

	return js('Confirmation email has been sent.', 201)


@auth.route('/registration/confirm', methods=['GET'])
def confirm_registration():
	token = request.args.get('token')

	if not token:
		return 'Token missing.', 400

	data = decode_token(token)
	message, status_code = validate_confirm_registration_data(data=data)

	if not succ_status(code=status_code):
		return message, status_code

	new_user = User(public_id=uuid4(), email=data['email'], password=data['password'])
	
	try:
		db.session.add(new_user)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return 'Internal Server Error.', 500

	send_reg_confirmed_mail(recipient=data['email'])

	return 'Registration confirmed.', 200


@auth.route('/registration', methods=['DELETE'])
@token_required
def cancel_registration(current_user):
	payload = {'public_id': current_user.public_id}
	token = encode_token(payload=payload, lifetime=app.config['CANCEL_REGISTRATION_TOKEN_LIFETIME'])
	
	send_cancel_reg_confirm_email(recipient=current_user.email, token=token.decode('utf-8'))
	
	return js('Confirmation email has been sent.', 202)


@auth.route('/registration/cancel/confirm', methods=['GET'])
def confirm_cancel_registration():
	token = request.args.get('token')

	if not token:
		return 'Token missing.', 400

	payload = decode_token(token)

	if not payload:
		return 'Token invalid.', 400

	if payload.get('expiresAt') and float(payload['expiresAt']) < time():
		return 'Token expired.', 400

	user = User.query.filter_by(public_id=payload.get('public_id')).first()

	if not user:
		return 'Token invalid.', 400

	email = user.email

	try:
		db.session.delete(user)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return 'Internal Server Error.', 500

	send_cancel_reg_confirmed_email(recipient=email)

	return 'Registration cancelled.', 200


@auth.route('/login', methods=['POST'])
def login():
	data = request.get_json()

	message, status_code = validate_login(data)

	if not succ_status(code=status_code):
		return js(message, status_code)

	user = User.query.filter_by(email=data['email']).first()

	payload = {'public_id': user.public_id}
	token = encode_token(payload=payload, lifetime=app.config['LOGIN_TOKEN_LIFETIME'])

	return jsonify({'token': token.decode('utf-8')}), 201


@auth.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
	"""blacklist token"""
	pass

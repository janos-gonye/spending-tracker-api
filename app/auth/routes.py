from uuid import uuid4

from flask import jsonify, request, current_app as app
from werkzeug.security import generate_password_hash

from app.auth import auth
from app.auth.mail import send_reg_confirm_mail
from app.auth.utils import validate_registration_data
from app.utils.token import gen_token


@auth.route('/registration', methods=['POST'])
def registration():
	data = request.get_json()

	json, status_code = validate_registration_data(data=data)

	if status_code != 200:
		return json, status_code

	payload = {'email': data['email'], 'password': data['password']}
	token = gen_token(payload=payload, lifetime=app.config['REGISTRATION_TOKEN_LIFETIME'])
	
	send_reg_confirm_mail(recipient=data['email'], token=token.decode('utf-8'))

	return jsonify({'message': 'Confirmation email has been sent.'}), 200


@auth.route('/registration/confirm', methods=['GET'])
def confirm_registration():
	token = request.args.get('token')

	return 'Registration confirmed.'


@auth.route('/registration', methods=['DELETE'])
def delete_registration():
	return 'Reg'


@auth.route('/login', methods=['POST'])
def login():
	pass
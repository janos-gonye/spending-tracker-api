from time import time
from uuid import uuid4
# Use uuid4 bacause uuid1() may compromise privacy since it creates a UUID
# containing the computer’s network address. uuid4() creates a random UUID.

from flask import current_app as app
from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.auth import auth
from app.auth.decorators import token_required
from app.auth.mail import (send_cancel_reg_confirm_email,
                           send_cancel_reg_confirmed_email,
                           send_reg_confirm_mail, send_reg_confirmed_mail)
from app.auth.models import User
from app.auth.validators import (validate_change_password,
                                 validate_confirm_registration_data,
                                 validate_login, validate_registration_data)
from app.common.decorators import jsonify_view
from app.common.token import decode_token, encode_token
from app.db import db


@auth.route('/registration', methods=['POST'])
@jsonify_view
def registration():
    data = request.get_json()

    validate_registration_data(data=data)

    payload = {'email': data['email'], 'password': data['password']}
    token = encode_token(
        payload=payload, lifetime=app.config['REGISTRATION_TOKEN_LIFETIME'])

    send_reg_confirm_mail(recipient=data['email'], token=token.decode('utf-8'))

    return 'Confirmation email has been sent.', 202


@auth.route('/registration/confirm', methods=['GET'])
def confirm_registration():
    token = request.args.get('token')

    if not token:
        return 'Token missing.', 400

    data = decode_token(token)
    validate_confirm_registration_data(data=data)

    new_user = User(public_id=uuid4(),
                    email=data['email'], password=data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500

    send_reg_confirmed_mail(recipient=data['email'])

    return 'Registration confirmed.', 200


@auth.route('/registration', methods=['DELETE'])
@jsonify_view
@token_required
def cancel_registration(current_user):
    payload = {'public_id': current_user.public_id}
    token = encode_token(
        payload=payload,
        lifetime=app.config['CANCEL_REGISTRATION_TOKEN_LIFETIME'])

    send_cancel_reg_confirm_email(
        recipient=current_user.email, token=token.decode('utf-8'))

    return 'Confirmation email has been sent.', 202


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
@jsonify_view
def login():
    data = request.get_json()

    validate_login(data)

    user = User.query.filter_by(email=data['email']).first()

    payload = {'public_id': user.public_id}
    token = encode_token(
        payload=payload, lifetime=app.config['LOGIN_TOKEN_LIFETIME'])

    return None, 201, {'token': token.decode('utf-8')}


@auth.route('/verify-token', methods=['GET'])
@jsonify_view
@token_required
def token_valid(self):
    return 'Token valid.'


@auth.route('/logout', methods=['POST'])
@jsonify_view
@token_required
def logout(current_user):
    """blacklist token"""
    pass


@auth.route('/change-password', methods=['POST'])
@jsonify_view
@token_required
def change_password(current_user):
    data = request.get_json()

    validate_change_password(data, current_user)

    new_password = data['new_password']

    try:
        current_user.set_password(new_password)
        db.session.commit()
        return 'Password changed.', 200
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500

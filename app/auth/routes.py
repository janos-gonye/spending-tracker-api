from time import time
from uuid import uuid4
# Use uuid4 bacause uuid1() may compromise privacy since it creates a UUID
# containing the computer’s network address. uuid4() creates a random UUID.

from flask import current_app as app
from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.auth import auth, mail, validators
from app.auth.decorators import token_required
from app.auth.models import User
from app.common.decorators import jsonify_view
from app.common.helpers import generate_password
from app.common.token import TokenTypes, decode_token, encode_token
from app.db import db


@auth.route('/registration', methods=['POST'])
@jsonify_view
@validators.registration
def registration(data):
    payload = {'email': data['email'], 'password': data['password']}
    token = encode_token(
        payload=payload, token_type=TokenTypes.REGISTRATION,
        lifetime=app.config['REGISTRATION_TOKEN_LIFETIME'])

    mail.send_reg_confirm_mail(recipient=data['email'], token=token.decode('utf-8'))

    return 'Confirmation email has been sent.', 202


@auth.route('/registration/confirm', methods=['GET'])
@validators.confirm_registration
def confirm_registration(data):
    new_user = User(public_id=uuid4(),
                    email=data['email'], password=data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500

    mail.send_reg_confirmed_mail(recipient=data['email'])

    return 'Registration confirmed.', 200


@auth.route('/registration', methods=['DELETE'])
@jsonify_view
@token_required
def cancel_registration(current_user):
    payload = {'public_id': current_user.public_id}
    token = encode_token(
        payload=payload, token_type=TokenTypes.CANCEL_REGISTRATION,
        lifetime=app.config['CANCEL_REGISTRATION_TOKEN_LIFETIME'])

    mail.send_cancel_reg_confirm_email(
        recipient=current_user.email, token=token.decode('utf-8'))

    return 'Confirmation email has been sent.', 202


@auth.route('/registration/cancel/confirm', methods=['GET'])
@validators.confirm_cancel_registration
def confirm_cancel_registration(data):
    user = User.query.filter_by(public_id=data.get('public_id')).first()

    if not user:
        return 'Token invalid.', 400

    email = user.email

    try:
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500

    mail.send_cancel_reg_confirmed_email(recipient=email)

    return 'Registration cancelled.', 200


@auth.route('/login', methods=['POST'])
@jsonify_view
@validators.login
def login(data):
    user = User.query.filter_by(email=data['email']).first()

    payload = {'public_id': user.public_id}
    access_token = encode_token(
        payload=payload, token_type=TokenTypes.ACCESS,
        lifetime=app.config['LOGIN_TOKEN_LIFETIME'])
    payload = {'public_id': user.public_id}
    refresh_token = encode_token(
        payload=payload, token_type=TokenTypes.REFRESH,
        lifetime=app.config['REFRESH_TOKEN_LIFETIME'])

    return None, 201, {
        'access_token': access_token.decode('utf-8'),
        'refresh_token': refresh_token.decode('utf-8')
    }


@auth.route('/refresh-token', methods=['POST'])
@jsonify_view
@validators.refresh_token
def refresh_token(data):
    payload = decode_token(data['refresh_token'], TokenTypes.REFRESH)

    if payload.get('expiresAt') and payload['expiresAt'] < time():
        return 'Session expired.', 401, {"expired": True}

    payload = {'public_id': payload['public_id']}
    access_token = encode_token(
        payload=payload, token_type=TokenTypes.ACCESS,
        lifetime=app.config['LOGIN_TOKEN_LIFETIME'])
    
    return None, 201, {
        'access_token': access_token.decode('utf-8')
    }


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
@validators.change_password
def change_password(data, current_user):
    new_password = data['new_password']

    try:
        current_user.set_password(new_password)
        db.session.commit()
        return 'Password changed.', 200
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500


@auth.route('/forgot-password', methods=['POST'])
@jsonify_view
@validators.forgot_password
def forgot_password(data):
    email = data['email']
    payload = {'email': email}
    token = encode_token(
        payload=payload, token_type=TokenTypes.RESET_PASSWORD,
        lifetime=app.config['RESET_PASSWORD_TOKEN_LIFETIME'])

    mail.send_reset_password_mail(recipient=email, token=token.decode('utf-8'))

    return 'Email to reset your password sent.', 202


@auth.route('/reset-password', methods=['GET'])
@validators.reset_password
def reset_password(data):
    email = data.get('email')
    if not email:
        return 'Token invalid.', 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return 'Token invalid.', 400

    new_password = generate_password()

    try:
        user.set_password(new_password)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500

    mail.send_new_password_mail(recipient=email, new_password=new_password)

    return 'Email with new password sent.', 202

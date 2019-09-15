from time import time

from app.auth.models import User
from app.common.exceptions import ValidationError
from app.common.templates import json_validator_template
from app.common.validators import validate_email, validate_password


def _validate_registration(data):
    email = data.get('email')
    password = data.get('password')

    if not email and not password:
        raise ValidationError('Email and password missing.')

    if not email:
        raise ValidationError('Email missing.')

    validate_email(email)
    validate_password(password)

    if email and already_registered(email=email):
        raise ValidationError('Email address already registered.')


def validate_confirm_registration(data):
    """doesn't check if user already registered"""

    try:
        _validate_registration(data=data)
    except ValidationError:
        raise ValidationError('Token invalid.', 401)

    if already_registered(email=data['email']):
        # this time with a different message
        raise ValidationError('Registration already confirmed.')

    expiresAt = data.get('expiresAt')
    if expiresAt and float(expiresAt) < time():
        raise ValidationError('Token expired.')


def already_registered(email):
    return bool(User.query.filter_by(email=email).first())


def _validate_login(data):

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise ValidationError('Invalid credentials.', 401)

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        raise ValidationError('Invalid credentials.', 401)


def _validate_change_password(data, current_user):
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password:
        raise ValidationError('Old password missing.')

    if not new_password:
        raise ValidationError('New password missing.')

    if not current_user.check_password(old_password):
        raise ValidationError('Invalid credentials.', 401)

    validate_password(new_password)


def _validate_forgot_password(data):
    email = data.get('email')

    if not email:
        raise ValidationError('Email missing.')

    if not User.query.filter_by(email=email).first():
        raise ValidationError('Email not found.', 404)


validate_registration = json_validator_template(_validate_registration)
validate_login = json_validator_template(_validate_login)
validate_change_password = json_validator_template(_validate_change_password)
validate_forgot_password = json_validator_template(_validate_forgot_password)

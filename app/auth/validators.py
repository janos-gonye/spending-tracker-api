from time import time

from app.auth.models import User
from app.common.decorators import require_json_validator
from app.common.exceptions import ValidationError
from app.common.validators import validate_email, validate_password


@require_json_validator
def validate_registration_data(data):
    """doesn't check if user already registered"""

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


def validate_confirm_registration_data(data):
    """doesn't check if user already registered"""

    try:
        validate_registration_data(data=data)
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


@require_json_validator
def validate_login(data):

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise ValidationError('Invalid credentials.', 401)

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        raise ValidationError('Invalid credentials.', 401)


@require_json_validator
def validate_change_password(data, user):
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password:
        raise ValidationError('Old password missing.')

    if not new_password:
        raise ValidationError('New password missing.')

    if not user.check_password(old_password):
        raise ValidationError('Invalid credentials.', 401)

    validate_password(new_password)


@require_json_validator
def validate_forgot_password_data(data):
    email = data.get('email')

    if not email:
        raise ValidationError('Email missing.')

    if not User.query.filter_by(email=email).first():
        raise ValidationError('Email not found.', 404)

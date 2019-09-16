import re

from flask import current_app as app

from app.common.exceptions import ValidationError

EMAIL_REGEX = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'


def validate_password(password):
    length = len(password)
    min_l = app.config['PASSWORD_MIN_LEN']
    max_l = app.config['PASSWORD_MAX_LEN']

    if length < min_l or length > max_l or \
       not re.search(r"[a-z]", password) or \
       not re.search(r"[A-Z]", password) or \
       not re.search(r"[0-9]", password):
        raise ValidationError(
            f"Password length must be {min_l}-{max_l} characters. "
            "It must contain at least one number, "
            "upper and lower case letters."
        )


def validate_email(email):
    if not bool(re.match(EMAIL_REGEX, email)):
        raise ValidationError('Invalid email address.')


def validate_int(x, name='value'):
    if isinstance(x, int):
        return x
    raise ValidationError(f"{name} is not an integer.")


def validate_natural_number(x, name='value'):
    try:
        validate_int(x)
        if not str(x).isdigit():
            raise ValueError()
        return x
    except (ValidationError, ValueError):
        raise ValidationError(f"{name} is not a valid natural number.")


def validate_bool(x, name='value'):
    if isinstance(x, bool):
        return x
    raise ValidationError(f"{name} is not a boolean value.")

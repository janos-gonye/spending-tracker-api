import re

from app.common.exceptions import ValidationError

EMAIL_REGEX = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'


def validate_password(password, min_length=6, max_length=50,
                      contain_lower=True, contain_upper=True,
                      contain_number=True):
    length = len(password)

    if length < min_length or length > max_length or \
       contain_lower and not re.search(r"[a-z]", password) or \
       contain_upper and not re.search(r"[A-Z]", password) or \
       contain_number and not re.search(r"[0-9]", password):
        raise ValidationError(
            f"Password's length must be at least {min_length} characters. "
            "Must contain number, upper and lower case letters.")


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

import time

from app.common import is_float, is_int, is_timestamp, key_exists
from app.common.decorators import require_json_validator
from app.common.exceptions import ValidationError
from app.transactions.models import Transaction

MIN_COMMENT_LEN = Transaction.MIN_COMMENT_LEN
MAX_COMMENT_LEN = Transaction.MAX_COMMENT_LEN


@require_json_validator
def validate_create_trans_data(data):

    # use this as data.get(...) would give None
    # wether key is not in JSON or key's value is NULL
    amount_in_json, amount = key_exists(data=data, key='amount')
    processed_at_in_json, processed_at = key_exists(
        data=data, key='processed_at')
    comment_in_json, comment = key_exists(data=data, key='comment')

    if amount_in_json:
        if not amount:
            raise ValidationError('Amount may not be <null>.')
        elif not is_float(amount):
            raise ValidationError('Amount must be a <float> number.')
    else:
        raise ValidationError('Amount required.')

    if processed_at_in_json:
        if not processed_at:
            raise ValidationError('Process datetime may not be <null>.')
        if not is_timestamp(processed_at):
            raise ValidationError('Process datetime must be UNIX timestamp.')
        elif float(processed_at) > time.time():
            raise ValidationError('Process datetime cannot be in future.')
    else:
        raise ValidationError('Process datetime is required.')

    if comment_in_json and comment and not (
       MIN_COMMENT_LEN < len(str(comment)) < MAX_COMMENT_LEN):
        raise ValidationError(
            'Comment must be at least %s max %s characters long.' % (
                MIN_COMMENT_LEN, MAX_COMMENT_LEN))


@require_json_validator
def validate_update_trans_data(data):

    # use this as data.get(...) would give None
    # wether key is not in JSON or key's value is NULL
    amount_in_json, amount = key_exists(data=data, key='amount')
    processed_at_in_json, processed_at = key_exists(
        data=data, key='processed_at')
    comment_in_json, comment = key_exists(data=data, key='comment')

    if amount_in_json:
        if not amount:
            raise ValidationError('Amount may not be <null>.')
        elif not is_float(amount):
            raise ValidationError('Amount must be a <float> number.')

    if processed_at_in_json:
        if not processed_at:
            raise ValidationError('Process datetime may not be <null>.')
        if not is_timestamp(processed_at):
            raise ValidationError('Process datetime must be UNIX timestamp.')
        elif float(processed_at) > time.time():
            raise ValidationError('Process datetime cannot be in future.')

    if comment_in_json and comment and not (
       MIN_COMMENT_LEN < len(str(comment)) < MAX_COMMENT_LEN):
        raise ValidationError(
            'Comment must be at least %s max %s characters long.' % (
                MIN_COMMENT_LEN, MAX_COMMENT_LEN))

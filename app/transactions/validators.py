import time

from app.transactions.models import Transaction
from app.utils import key_exists, is_timestamp, is_int, is_float


MIN_COMMENT_LEN = Transaction.MIN_COMMENT_LEN
MAX_COMMENT_LEN = Transaction.MAX_COMMENT_LEN


def validate_create_trans_data(data):
    if not data:
        return 'JSON payload required.', 400
    # use this as data.get(...) would give None
    # wether key is not in JSON or key's value is NULL
    amount_in_json, amount = key_exists(data=data, key='amount')
    processed_at_in_json, processed_at = key_exists(
        data=data, key='processed_at')
    comment_in_json, comment = key_exists(data=data, key='comment')
    if amount_in_json:
        if not amount:
            return 'Amount may not be <null>.', 400
        elif not is_float(amount):
            return 'Amount must be a <float> number.', 400
    else:
        return 'Amount required.', 400
    if processed_at_in_json:
        if not processed_at:
            return 'Process datetime may not be <null>.', 400
        if not is_timestamp(processed_at):
            return 'Process datetime must be UNIX timestamp.', 400
        elif float(processed_at) > time.time():
            return 'Process datetime cannot be in future.', 400
    else:
        return 'Process datetime is required.', 400
    if comment_in_json and comment and not (
       MIN_COMMENT_LEN < len(str(comment)) < MAX_COMMENT_LEN):
        return 'Comment must be at least %s max %s characters long.' % (
            MIN_COMMENT_LEN, MAX_COMMENT_LEN), 400
    return 'Transaction valid.', 200


def validate_update_trans_data(data):
    if not data:
        return 'JSON payload required.', 400
    # use this as data.get(...) would give None
    # wether key is not in JSON or key's value is NULL
    amount_in_json, amount = key_exists(data=data, key='amount')
    processed_at_in_json, processed_at = key_exists(
        data=data, key='processed_at')
    comment_in_json, comment = key_exists(data=data, key='comment')
    if amount_in_json:
        if not amount:
            return 'Amount may not be <null>.', 400
        elif not is_float(amount):
            return 'Amount must be a <float> number.', 400
    if processed_at_in_json:
        if not processed_at:
            return 'Process datetime may not be <null>.', 400
        if not is_timestamp(processed_at):
            return 'Process datetime must be UNIX timestamp.', 400
        elif float(processed_at) > time.time():
            return 'Process datetime cannot be in future.', 400
    if comment_in_json and comment and not (
       MIN_COMMENT_LEN < len(str(comment)) < MAX_COMMENT_LEN):
        return 'Comment must be at least %s max %s characters long.' % (
            MIN_COMMENT_LEN, MAX_COMMENT_LEN), 400
    return 'Transaction valid.', 200

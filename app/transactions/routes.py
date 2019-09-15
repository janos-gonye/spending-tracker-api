from datetime import datetime

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.auth.decorators import token_required
from app.categories.decorators import get_category_or_404
from app.common import datetime2timestamp, key_exists, timestamp2datetime
from app.common.decorators import jsonify_view
from app.common.params import get_param_from, get_param_to
from app.db import db
from app.transactions import trans_blueprint, validators
from app.transactions.decorators import get_trans_or_404
from app.transactions.models import Transaction


@trans_blueprint.route('', methods=['POST'])
@jsonify_view
@token_required
@get_category_or_404
@validators.create_transaction
def create_transaction(data, current_user, cat):
    amount = data.get('amount')
    processed_at = data.get('processed_at')
    comment = data.get('comment')

    new_trans = Transaction(amount=amount,
                            processed_at=timestamp2datetime(processed_at),
                            comment=comment,
                            category_id=cat.id)

    try:
        db.session.add(new_trans)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Unternal Server Error.', 500

    return new_trans.as_dict(), 201, {'key': 'transaction'}


@trans_blueprint.route('', methods=['GET'])
@jsonify_view
@token_required
@get_category_or_404
def get_transactions(current_user, cat):
    try:
        from_ = get_param_from()
        to = get_param_to()
    except ValueError as err:
        return str(err), 400
    if cat == '__all__':
        trans_s = []
        for cat in current_user.categories:
            trans_s += cat.transactions
    else:
        trans_s = cat.get_transactions(children=True)

    trans_s = filter(
        lambda t: from_ <= datetime2timestamp(t.processed_at) <= to, trans_s)

    return [trans.as_dict() for trans in trans_s], 200, {'key': 'transactions'}


@trans_blueprint.route('/<int:trans_id>', methods=['GET'])
@jsonify_view
@token_required
@get_category_or_404
@get_trans_or_404
def get_transaction(current_user, cat, trans):
    return trans.as_dict(), 200, {'key': 'transaction'}


@trans_blueprint.route('/<int:trans_id>', methods=['PATCH'])
@jsonify_view
@token_required
@get_category_or_404
@get_trans_or_404
@validators.update_transaction
def update_transaction(data, current_user, cat, trans):
    amount_in_json, amount = key_exists(data=data, key='amount')
    processed_at_in_json, processed_at = key_exists(
        data=data, key='processed_at')
    comment_in_json, comment = key_exists(data=data, key='comment')

    # if any of them changed
    if amount_in_json and float(trans.amount) != float(amount) or \
       comment_in_json and trans.comment != comment or \
       processed_at_in_json and \
       (processed_at != datetime2timestamp(trans.processed_at)):
        trans.updated_at = datetime.utcnow()

    if amount_in_json:
        trans.amount = amount
    if processed_at_in_json:
        trans.processed_at = timestamp2datetime(processed_at)
    if comment_in_json:
        trans.comment = comment

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error.', 500

    return trans.as_dict(), 200, {'key': 'transaction'}


@trans_blueprint.route('/<int:trans_id>', methods=['DELETE'])
@jsonify_view
@token_required
@get_category_or_404
@get_trans_or_404
def delete_transaction(current_user, cat, trans):
    try:
        db.session.delete(trans)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error', 500

    return trans.as_dict(), 200, {'key': 'transaction'}

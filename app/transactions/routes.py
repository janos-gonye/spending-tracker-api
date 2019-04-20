from datetime import datetime

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.auth.decorators import token_required
from app.categories.decorators import get_category_or_404
from app.db import db
from app.transactions import trans_blueprint
from app.transactions.decorators import get_trans_or_404
from app.transactions.models import Transaction
from app.transactions.validators import validate_create_trans_data
from app.transactions.validators import validate_update_trans_data
from app.utils import js, succ_status, key_exists, timestamp2datetime, datetime2timestamp


@trans_blueprint.route('', methods=['POST'])
@token_required
@get_category_or_404
def create_transaction(current_user, cat):
	data = request.get_json()

	message, status_code = validate_create_trans_data(data=data)

	if not succ_status(code=status_code):
		return js(message, status_code)

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
		return js('Unternal Server Error.', 500)

	return js(new_trans.as_dict(), 201, key='transaction')


@trans_blueprint.route('', methods=['GET'])
@token_required
@get_category_or_404
def get_transactions(current_user, cat):
	trans_s = Transaction.query.filter_by(category_id=cat.id).all()
	return js([trans.as_dict() for trans in trans_s], 200, 'transactions')


@trans_blueprint.route('/<int:trans_id>', methods=['GET'])
@token_required
@get_category_or_404
@get_trans_or_404
def get_transaction(current_user, cat, trans):
	return js(trans.as_dict(), 200, 'transaction')


@trans_blueprint.route('/<int:trans_id>', methods=['PATCH'])
@token_required
@get_category_or_404
@get_trans_or_404
def update_transaction(current_user, cat, trans):
	data = request.get_json()
	message, status_code = validate_update_trans_data(data=data)

	if not succ_status(code=status_code):
		return js(message, status_code)

	amount_in_json, amount = key_exists(data=data, key='amount')
	processed_at_in_json, processed_at = key_exists(data=data, key='processed_at')
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
		return js('Internal Server Error.', 500)

	return js(trans.as_dict(), 200, 'transaction')


@trans_blueprint.route('/<int:trans_id>', methods=['DELETE'])
@token_required
@get_category_or_404
@get_trans_or_404
def delete_transaction(current_user, cat, trans):
	try:
		db.session.delete(trans)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return js('Internal Server Error', 500)

	return js(trans.as_dict(), 200, 'transaction')

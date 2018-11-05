from datetime import datetime

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.auth.decorators import token_required
from app.categories import cat_blueprint
from app.categories.decorators import get_category_or_404
from app.categories.models import Category
from app.categories.validators import validate_create_category_data
from app.categories.validators import validate_update_category_data
from app.db import db
from app.utils import js, succ_status


@cat_blueprint.route('', methods=['POST'])
@token_required
def create_category(current_user):
	data = request.get_json()

	message, status_code = validate_create_category_data(user=current_user,
														 data=data)
	if not succ_status(code=status_code):
		return js(message, status_code)

	title = data.get('title')
	description = data.get('description')
	parent_id = data.get('parent_id')

	new_cat = Category(title=title,
					   description=description,
					   user_id=current_user.id,
					   parent_id=parent_id)

	try:
		db.session.add(new_cat)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return js('Internal Server Error.', 500)

	return js(new_cat.as_dict(), 201, key='category')


@cat_blueprint.route('', methods=['GET'])
@token_required
def get_categories(current_user):
	cats = Category.query.filter_by(parent_id=None, user_id=current_user.id).all()
	return js([cat.as_dict() for cat in cats], 200, 'categories')


@cat_blueprint.route('<int:id>', methods=['GET'])
@token_required
@get_category_or_404
def get_category(current_user, cat, id):
	return js(cat.as_dict(), 200, 'category')


@cat_blueprint.route('<int:id>', methods=['PATCH'])
@token_required
@get_category_or_404
def update_category(current_user, cat, id):
	data = request.get_json()
	message, status_code = validate_update_category_data(data=data,
														 user=current_user,
														 cat_to_change=cat)
	if not succ_status(code=status_code):
		return js(message, status_code)

	title = data.get('title')
	description = data.get('title')
	parent_id = data.get('parent_id')

	# if any of them changed
	if cat.title != title or \
	   cat.description != description or \
	   cat.parent_id != parent_id:
		cat.updated_at = datetime.utcnow()

	cat.title = title if title else cat.title
	cat.description = description if description else cat.description
	cat.parent_id = parent_id if parent_id else cat.parent_id

	try:
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return js('Internal Server Error', 500)

	return js(cat.as_dict(), 200, 'category')


@cat_blueprint.route('/<int:id>', methods=['DELETE'])
@token_required
@get_category_or_404
def delete_category(current_user, cat, id):
	try:
		db.session.delete(cat)
		db.session.commit()
	except SQLAlchemyError:
		db.session.rollback()
		return js('Internal Server Error', 500)

	return js(cat.as_dict(), 200, 'category')

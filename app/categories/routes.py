from datetime import datetime

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from app.auth.decorators import token_required
from app.categories import cat_blueprint
from app.categories.decorators import get_category_or_404
from app.categories.models import Category
from app.categories.validators import (validate_create_category_data,
                                       validate_update_category_data)
from app.common import key_exists
from app.common.decorators import jsonify_view
from app.db import db


@cat_blueprint.route('', methods=['POST'])
@jsonify_view
@token_required
def create_category(current_user):
    data = request.get_json()

    validate_create_category_data(user=current_user, data=data)

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
        return 'Internal Server Error.', 500

    return new_cat.as_dict(), 201, {'key': 'category'}


@cat_blueprint.route('', methods=['GET'])
@jsonify_view
@token_required
def get_categories(current_user):
    cats = Category.query.filter_by(user_id=current_user.id).all()
    cats.sort(key=lambda c: c.history)
    return [cat.as_dict() for cat in cats], 200, {'key': 'categories'}


@cat_blueprint.route('<int:cat_id>', methods=['GET'])
@jsonify_view
@token_required
@get_category_or_404
def get_category(current_user, cat):
    return cat.as_dict(), 200, {'key': 'category'}


@cat_blueprint.route('<int:cat_id>', methods=['PATCH'])
@jsonify_view
@token_required
@get_category_or_404
def update_category(current_user, cat):
    data = request.get_json()
    validate_update_category_data(data=data, user=current_user,
                                  cat_to_change=cat)

    title = data.get('title')
    description_in_json, description = key_exists(data=data, key='description')
    parent_id_in_json, parent_id = key_exists(data=data, key='parent_id')

    # if any of them changed
    if cat.title != title or \
       description_in_json and cat.description != description or \
       parent_id_in_json and cat.parent_id != parent_id:
        cat.updated_at = datetime.utcnow()

    cat.title = title if title else cat.title
    if description_in_json:
        cat.description = description
    if parent_id_in_json:
        cat.parent_id = parent_id

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error', 500

    return cat.as_dict(), 200, {'key': 'category'}


@cat_blueprint.route('/<int:cat_id>', methods=['DELETE'])
@jsonify_view
@token_required
@get_category_or_404
def delete_category(current_user, cat):
    try:
        db.session.delete(cat)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return 'Internal Server Error', 500

    return cat.as_dict(), 200, {'key': 'category'}

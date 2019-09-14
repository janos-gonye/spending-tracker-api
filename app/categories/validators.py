from app.categories.models import Category
from app.common import key_exists
from app.common.decorators import require_json_validator
from app.common.exceptions import ValidationError
from app.common.validators import (validate_bool, validate_int,
                                   validate_natural_number)

MIN_TITLE_LEN = Category.MIN_TITLE_LEN
MAX_TITLE_LEN = Category.MAX_TITLE_LEN
MIN_DESCRIPTION_LEN = Category.MIN_DESCRIPTION_LEN
MAX_DESCRIPTION_LEN = Category.MAX_DESCRIPTION_LEN


@require_json_validator
def validate_create_category(data, user):

    # use this as data.get(...) would give None
    # whether key is not in JSON or key's value is null
    title_in_json, title = key_exists(data=data, key='title')
    description_in_json, description = key_exists(data=data, key='description')
    parent_id_in_json, parent_id = key_exists(data=data, key='parent_id')

    if title_in_json:
        if not title:
            raise ValidationError('Title may not be <null>.')
        elif not MIN_TITLE_LEN <= len(title) <= MAX_TITLE_LEN:
            raise ValidationError(
                'Title must be at least %s max %s characters long.' % (
                    MIN_TITLE_LEN, MAX_TITLE_LEN))
    else:
        raise ValidationError('Title required.')

    if description_in_json:
        if description is None:
            raise ValidationError('Description may not be <null>.')
        elif not (
             MIN_DESCRIPTION_LEN <= len(description) <= MAX_DESCRIPTION_LEN):
            raise ValidationError((
                'Description must be at least %s max %s characters long.' %
                (MIN_DESCRIPTION_LEN, MAX_DESCRIPTION_LEN)))

    # Not necessary to check if <parent_id> is int (or can be converted to int)
    # because <filter_by> also finds integer ids as strings.
    if parent_id_in_json and parent_id and not Category.query.filter_by(
       id=parent_id, user_id=user.id).first():
        raise ValidationError("Parent doesn't exist.")

    unique_together = not Category.query.filter_by(user_id=user.id,
                                                   parent_id=parent_id,
                                                   title=title).first()
    if not unique_together:
        raise ValidationError('Title and parent_id must be unique together.')


@require_json_validator
def validate_update_category(data, user, cat_to_change):

    # use this as data.get(...) would give None
    # whether key is not in JSON or key's value is null
    title_in_json, title = key_exists(data=data, key='title')
    description_in_json, description = key_exists(data=data, key='description')
    parent_id_in_json, parent_id = key_exists(data=data, key='parent_id')

    if title_in_json:
        if not title:
            raise ValidationError('Title may not be <null>.')
        elif not MIN_TITLE_LEN <= len(title) <= MAX_TITLE_LEN:
            raise ValidationError(
                'Title must be at least %s max %s characters long.' % (
                    MIN_TITLE_LEN, MAX_TITLE_LEN))

    if description_in_json:
        if description is None:
            raise ValidationError('Description may not be <null>.')
        elif not (
             MIN_DESCRIPTION_LEN <= len(description) <= MAX_DESCRIPTION_LEN):
            raise ValidationError(
                'Description must be at least %s max %s characters long.' %
                (MIN_DESCRIPTION_LEN, MAX_DESCRIPTION_LEN))

    if parent_id_in_json and parent_id is not None:
        if not Category.query.filter_by(id=parent_id, user_id=user.id).first():
            raise ValidationError("Parent doesn't exist.")
        elif int(parent_id) == cat_to_change.id:
            raise ValidationError("Parent may not be itself.")
        elif int(parent_id) in map(
             lambda child: child.id, cat_to_change.get_descendents()):
            raise ValidationError(
                "Parent may not be descendent of the category being updated.")

    ti = title if title_in_json and title else cat_to_change.title
    pi = parent_id if parent_id_in_json and parent_id else\
        cat_to_change.parent_id

    cats = Category.query.filter_by(user_id=user.id,
                                    title=ti,
                                    parent_id=pi).all()

    for cat in cats:
        # if not the category to change itself
        # then it breaks the unique together constraint
        if cat is not cat_to_change:
            raise ValidationError(
                'Title and parent_id must be unique together.')


@require_json_validator
def validate_merge_categories(data, user):
    subject_in_json, subject_id = key_exists(data=data, key='subject_id')
    target_in_json, target_id = key_exists(data=data, key='target_id')

    for key, name in (
        (subject_in_json, "'subject_id'"),
        (target_in_json, "'target_id'")):
        if not key:
            raise ValidationError(f"{name} missing.")

    subject_id = validate_natural_number(subject_id, name="'subject_id")
    target_id = validate_natural_number(target_id, name="'target_id")

    subject = Category.query.filter_by(user_id=user.id, id=subject_id).first()
    target = Category.query.filter_by(user_id=user.id, id=target_id).first()

    if not subject:
        raise ValidationError("Subject category not found.", 404)
    if not target:
        raise ValidationError("Target category not found.", 404)
    if subject_id == target_id:
        raise ValidationError("Category cannot be merged into itself.")

    for ascendent in target.get_ascendants():
        if ascendent.id == subject.id:
            raise ValidationError(
                "Category cannot be merged into any of its subcategories.")

from app.categories.models import Category
from app.utils import key_exists


MIN_TITLE_LEN = Category.MIN_TITLE_LEN
MAX_TITLE_LEN = Category.MAX_TITLE_LEN
MIN_DESCRIPTION_LEN = Category.MIN_DESCRIPTION_LEN
MAX_DESCRIPTION_LEN = Category.MAX_DESCRIPTION_LEN


def validate_create_category_data(user, data):
	if not data:
		return 'JSON payload required.', 400

	# use this as data.get(...) would give None whether key is not in JSON or key's value is null
	title_in_json, title = key_exists(data=data, key='title')
	description_in_json, description_in_json = key_exists(data=data, key='description')
	parent_id_in_json, parent_id = key_exists(data=data, key='parent_id')

	if title_in_json:
		if not title:
			return 'Title may not be <null>.', 400
		elif not MIN_TITLE_LEN < len(title) < MAX_TITLE_LEN:
			return 'Title must be at least %s max %s characters long.' % (
				MIN_TITLE_LEN, MAX_TITLE_LEN), 400
	else:
		return 'Title required.', 400

	if description_in_json:
		if not description:
			return 'Description may not be <null>.', 400
		elif not (MIN_DESCRIPTION_LEN < len(description) < MAX_DESCRIPTION_LEN):
			return 'Description must be at least %s max %s characters long.' % (
				MIN_DESCRIPTION_LEN, MAX_DESCRIPTION_LEN), 400

	# Not necessary to check if <parent_id> is int (or can be converted to int),
	# because <filter_by> also finds integer ids as strings.
	if parent_id_in_json and parent_id and not Category.query.filter_by(id=parent_id, user_id=user.id).first():
		return "Parent doesn't exist.", 400

	unique_together = not Category.query.filter_by(user_id=user.id,
												   parent_id=parent_id,
												   title=title).first()
	if not unique_together:
		return 'Title and parent_id must be unique together.', 400

	return 'Category valid.', 200


def validate_update_category_data(data, user, cat_to_change): 
	if not data:
		return 'JSON payload required.', 400

	# use this as data.get(...) would give None whether key is not in JSON or key's value is null
	title_in_json, title = key_exists(data=data, key='title')
	description_in_json, description = key_exists(data=data, key='description')
	parent_id_in_json, parent_id = key_exists(data=data, key='parent_id')

	if title_in_json:
		if not title:
			return 'Title may not be <null>.', 400
		elif not MIN_TITLE_LEN < len(title) < MAX_TITLE_LEN:
			return 'Title must be at least %s max %s characters long.' % (
				MIN_TITLE_LEN, MAX_TITLE_LEN), 400

	if description_in_json:
		if not description:
			return 'Description may not be <null>.', 400
		elif not (MIN_DESCRIPTION_LEN < len(description) < MAX_DESCRIPTION_LEN):
			return 'Description must be at least %s max %s characters long.' % (
				MIN_DESCRIPTION_LEN, MAX_DESCRIPTION_LEN), 400

	if parent_id_in_json:
		if not Category.query.filter_by(id=parent_id, user_id=user.id).first():
			return "Parent doesn't exist.", 400
		elif int(parent_id) == cat_to_change.id:
			return "Parent may not be itself.", 400

	ti = title if title_in_json and title else cat_to_change.title
	pi = parent_id if parent_id_in_json and parent_id else cat_to_change.parent_id

	cats = Category.query.filter_by(user_id=user.id,
									title=ti,
									parent_id=pi).all()

	for cat in cats:
		# if not the category to change itself then it breaks the unique together constraint
		if cat is not cat_to_change:
			return 'Title and parent_id must be unique together.', 400

	return 'Category valid.', 200

from functools import wraps

from flask import request

from app.categories.models import Category
from app.utils import js


def get_category_or_404(f):
	@wraps(f)
	def decorated(current_user, *args, **kwargs):
		cat = Category.query.filter_by(id=request.view_args['id'], user_id=current_user.id).first()
		if not cat:
			return js('Category not found.', 404)
		return f(current_user, cat, *args, **kwargs)

	return decorated

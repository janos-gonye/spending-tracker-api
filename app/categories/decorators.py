from functools import wraps
from urllib.parse import unquote

from flask import request, url_for

from app.categories.models import Category
from app.common import js


def get_category_or_404(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        # Special path used when requesting all transactions
        # that belong to 'current_user'
        special_path = unquote(
            url_for("transactions.get_transactions", cat_id="*"))
        param = request.view_args['cat_id']
        if type(param) is not int and not param.isdigit():
            if param == '*' and request.path == special_path\
               and request.method == "GET":
                return f(current_user, '__all__')
            return js('Category not found.', 404)
        try:
            cat = Category.query.filter_by(
                id=param, user_id=current_user.id)[0]
        except IndexError:
            return js('Category not found.', 404)
        return f(current_user, cat)
    return decorated

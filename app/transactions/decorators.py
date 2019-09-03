from functools import wraps

from flask import request

from app.transactions.models import Transaction


def get_trans_or_404(f):
    @wraps(f)
    def decorated(current_user, cat, *args, **kwargs):
        trans = Transaction.query.filter_by(
            id=request.view_args['trans_id'], category_id=cat.id).first()
        if not trans:
            return 'Transaction not found.', 404
        return f(current_user, cat, trans)
    return decorated

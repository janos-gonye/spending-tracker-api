from functools import wraps

from flask import request

from app.scheduled_trans.models import ScheduledTransaction


def get_scheduled_trans_or_404(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        scheduled_trans = ScheduledTransaction.query.filter_by(
            id=request.view_args['scheduled_trans_id']).first()
        if not scheduled_trans:
            return 'Scheduled transaction not found.', 404
        return f(current_user, scheduled_trans)
    return decorated

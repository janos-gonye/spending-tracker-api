import json

from dicttoxml import dicttoxml

from app.auth.decorators import token_required
from app.categories.models import Category
from app.common import timestamp2datetime
from app.common.decorators import jsonify_view
from app.common.params import get_param_from, get_param_to
from app.statistics import statistics_blueprint
from app.statistics.helpers import get_statistics as get_statistics_
from app.statistics.mail import send_statistics_export_mail


@statistics_blueprint.route('', methods=['GET'])
@jsonify_view
@token_required
def get_statistics(current_user):
    try:
        from_ = get_param_from()
        to = get_param_to()
    except ValueError as err:
        return str(err), 400
    statistics = get_statistics_(user=current_user, from_=from_, to=to)
    return statistics, 200, {'key': 'statistics'}


@statistics_blueprint.route('/export', methods=['GET'])
@jsonify_view
@token_required
def export_statistics(current_user):
    try:
        from_ = get_param_from()
        to = get_param_to()
    except ValueError as err:
        return str(err), 400
    statistics = get_statistics_(user=current_user, from_=from_, to=to)
    from_ = timestamp2datetime(timestamp=from_)
    to = timestamp2datetime(timestamp=to)
    fmt = "%Y-%m-%d"
    timerange_str = from_.strftime(fmt) + "_" + to.strftime(fmt)
    attachments = [
        {
            "filename": f"statistics_{timerange_str}.json",
            "content_type": "application/json",
            "data": json.dumps(statistics)
        },
        {
            "filename": f"statistics_{timerange_str}.xml",
            "content_type": "application/xml",
            "data": dicttoxml(statistics, custom_root='statistics',
                              attr_type=False)
        }
    ]
    send_statistics_export_mail(recipient=current_user.email,
                                attachments=attachments)
    return "Email sent.", 200

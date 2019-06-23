import json

from dicttoxml import dicttoxml

from app.auth.decorators import token_required
from app.categories.models import Category
from app.statistics import statistics_blueprint
from app.statistics.helpers import get_statistics as get_statistics_
from app.statistics.mail import send_statistics_export_mail
from app.utils import js
from app.utils.params import get_param_from, get_param_to


@statistics_blueprint.route('', methods=['GET'])
@token_required
def get_statistics(current_user):
    try:
        from_ = get_param_from()
        to = get_param_to()
    except ValueError as err:
        return js(str(err), 400)
    statistics = get_statistics_(user=current_user, from_=from_, to=to)
    return js(statistics, key="statistics")


@statistics_blueprint.route('/export', methods=['GET'])
@token_required
def export_statistics(current_user):
    try:
        from_ = get_param_from()
        to = get_param_to()
    except ValueError as err:
        return js(str(err), 400)
    statistics = get_statistics_(user=current_user, from_=from_, to=to)
    attachments = [
        {
            "filename": "statistics.json",
            "content_type": "application/json",
            "data": json.dumps(statistics)
        },
        {
            "filename": "statistics.xml",
            "content_type": "application/xml",
            "data": dicttoxml(statistics, custom_root='statistics',
                              attr_type=False)
        }
    ]
    send_statistics_export_mail(recipient=current_user.email,
                                attachments=attachments)
    return js("Email has been sent with statistics.")

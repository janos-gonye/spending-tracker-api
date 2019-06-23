from app.auth.decorators import token_required
from app.categories.models import Category
from app.statistics import statistics_blueprint
from app.statistics.helpers import get_statistics as get_statistics_
from app.utils import js


@statistics_blueprint.route('', methods=['GET'])
@token_required
def get_statistics(current_user):
    statistics = get_statistics_(user=current_user)
    return js(statistics, key="statistics")


@statistics_blueprint.route('/export', methods=['GET'])
@token_required
def export_statistics(current_user):
    return js("Works!")

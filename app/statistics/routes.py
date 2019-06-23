from app.auth.decorators import token_required
from app.statistics import statistics_blueprint

from app.utils import js


@statistics_blueprint.route('', methods=['GET'])
@token_required
def get_statistics(current_user):
    return js("Works!")


@statistics_blueprint.route('/export', methods=['GET'])
@token_required
def export_statistics(current_user):
    return js("Works!")

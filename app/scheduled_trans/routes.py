from app.auth.decorators import token_required
from app.common.decorators import jsonify_view
from app.scheduled_trans import scheduled_trans_blueprint


@scheduled_trans_blueprint.route('', methods=['POST'])
@jsonify_view
@token_required
def create_scheduled_trans(data, current_user):
    pass


@scheduled_trans_blueprint.route('', methods=['GET'])
@jsonify_view
@token_required
def get_scheduled_trans_s(current_user):
    pass


@scheduled_trans_blueprint.route('/<int:scheduled_trans_id', methods=['GET'])
@jsonify_view
@token_required
@get_scheduled_trans_or_404
def get_scheduled_trans(current_user, scheduled_trans):
    pass


@scheduled_trans_blueprint.route('/<int:scheduled_trans_id', methods=['PATCH'])
@jsonify_view
@token_required
@get_scheduled_trans_or_404
def update_scheduled_trans(current_user, scheduled_trans):
    pass


@scheduled_trans_blueprint.route('/<int:scheduled_trans_id',
                                 methods=['DELETE'])
@jsonify_view
@token_required
@get_scheduled_trans_or_404
def delete_scheduled_trans(current_user, scheduled_trans):
    pass

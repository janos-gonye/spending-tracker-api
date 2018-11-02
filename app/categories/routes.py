from app.auth.check import token_required
from app.categories import categories


###################
# Main Categories #
###################
@categories.route('/', methods=['POST'])
@token_required
def create_category(current_user):
	pass


@categories.route('/', methods=['GET'])
@token_required
def get_categories(current_user):
	pass


@categories.route('/<int:id_>', methods=['GET'])
@token_required
def get_category(current_user, id_):
	pass


@categories.route('/<int:id_>', methods=['PATCH'])
@token_required
def update_category(current_user, id_):
	pass


@categories.route('/<int:id_>', methods=['DELETE'])
@token_required
def delete_category(current_user, id_):
	pass


#################
# Subcategories #
#################
@categories.route('/<int:main_id>/sub_categories', methods=['POST'])
@token_required
def create_sub_category(current_user, main_id):
	pass


@categories.route('/<int:main_id>/sub_categories', methods=['GET'])
@token_required
def get_sub_categories(current_user, main_id):
	pass


@categories.route('/<int:main_id>/sub_categories/<int:sub_id>', methods=['GET'])
@token_required
def get_sub_category(current_user, main_id, sub_id):
	pass


@categories.route('/<int:main_id>/sub_categories/<int:sub_id>', methods=['PATCH'])
@token_required
def update_sub_category(current_user, main_id, sub_id):
	pass


@categories.route('/<int:main_id>/sub_categories/<int:sub_id>', methods=['DELETE'])
@token_required
def delete_sub_category(current_user, main_id, sub_id):
	pass

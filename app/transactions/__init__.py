from flask import Blueprint


def init_app(app):
	app.register_blueprint(trans_blueprint, url_prefix='/api/categories/<int:cat_id>/transactions')


trans_blueprint = Blueprint('transactions', __name__)
import app.transactions.routes

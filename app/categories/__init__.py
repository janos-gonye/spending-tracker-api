from flask import Blueprint


def init_app(app):
	app.register_blueprint(categories, url_prefix='/api/categories')


categories = Blueprint('categories', __name__)
import app.categories.routes

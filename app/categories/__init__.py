from flask import Blueprint


def init_app(app):
    app.register_blueprint(cat_blueprint, url_prefix='/api/categories')


cat_blueprint = Blueprint('categories', __name__)
import app.categories.routes

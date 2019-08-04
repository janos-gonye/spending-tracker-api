from flask import Blueprint


def init_app(app):
    app.register_blueprint(statistics_blueprint, url_prefix='/api/statistics')


statistics_blueprint = Blueprint('statistics', __name__)
import app.statistics.routes

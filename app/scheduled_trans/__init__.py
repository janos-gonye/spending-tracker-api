from flask import Blueprint


def init_app(app):
    app.register_blueprint(scheduled_trans_blueprint,
                           url_prefix='/api/scheduled-transactions')


scheduled_trans_blueprint = Blueprint('scheduled-trans', __name__)
import app.scheduled_trans.routes

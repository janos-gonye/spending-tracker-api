from flask import Blueprint


def init_app(app):
	app.register_blueprint(auth, url_prefix='/api/auth')

auth = Blueprint('auth', __name__)

import app.auth.routes

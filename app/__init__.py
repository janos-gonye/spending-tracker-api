from flask import Flask


def create_app():
	app = Flask(__name__)
	app.config.from_object('config')

	from . import auth, categories, db, transactions
	auth.init_app(app)
	db.init_app(app)
	categories.init_app(app)
	transactions.init_app(app)

	return app

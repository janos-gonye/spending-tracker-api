from flask import Flask


def create_app():
	app = Flask(__name__)
	app.config.from_object('config')

	from . import auth, db, categories, mail, transactions, statistics
	auth.init_app(app)
	db.init_app(app)
	categories.init_app(app)
	mail.init_app(app)
	transactions.init_app(app)
	statistics.init_app(app)

	return app

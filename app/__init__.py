from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    from . import auth, db, categories, mail, transactions, statistics,\
                  errors, scheduled_trans
    auth.init_app(app)
    db.init_app(app)
    categories.init_app(app)
    mail.init_app(app)
    transactions.init_app(app)
    statistics.init_app(app)
    errors.init_app(app)
    # scheduled_trans.init_app(app)

    return app

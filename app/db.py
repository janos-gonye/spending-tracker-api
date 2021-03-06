from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def init_app(app):
    migrate = Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()


db = SQLAlchemy()

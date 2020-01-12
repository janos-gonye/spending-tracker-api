from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

from app.categories.models import Category
from app.common import datetime2timestamp
from app.db import db


class AbstractTransaction(db.Model):
    __abstract__ = True

    MIN_COMMENT_LEN = 0
    MAX_COMMENT_LEN = 300

    # amount of money, + -> income, - -> outcome
    amount = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(MAX_COMMENT_LEN), default="")

    @declared_attr
    def category_id(cls):
        return db.Column(db.Integer, db.ForeignKey(
            'categories.id', ondelete='cascade'), nullable=False)

    @property
    def category(self):
        category = Category.query.filter_by(id=self.category_id).all()
        if len(category) == 0:
            return None
        return category[0]

    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'comment': self.comment,
            'category': self.category.as_dict(),
        }

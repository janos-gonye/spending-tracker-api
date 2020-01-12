from datetime import datetime

from app.common import datetime2timestamp
from app.common.models import AbstractTransaction


class Transaction(db.Model):
    __tablename__ = 'transactions'

    # when the money is earned or spent (stored as DateTime,
    # it's useful when creating financial reports)
    processed_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id', ondelete='cascade'), nullable=False)

    def as_dict(self):
        dict_ = super().as_dict()
        dict_['processed_at'] = datetime2timestamp(self.processed_at)
        return dict_

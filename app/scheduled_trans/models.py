from app.db import db
from app.db_fields import ChoiceType
from app.transactions.models import Transaction


class ScheduledTransaction(Transaction):
    __tablename__ = 'scheduled_transactions'

    frequency = db.Column(ChoiceType({
        "week": "week",
        "month": "month",
        "year": "year",
    }), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def as_dict(self):
        dict_ = super().as_dict()
        dict_['frequency'] = self.frequency,
        dict_['day'] = self.day,
        dict_['is_active'] = self.is_active
        return dict_

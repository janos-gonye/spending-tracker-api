from app.db import db
from app.db_fields import ChoiceType


class ScheduledTransaction(db.Model):
    __tablename__ = 'scheduled_transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.ChoiceTyp({
        "week": "week",
        "month": "month",
        "year": "year",
    }), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id', ondelete='cascade'), nullable=False)

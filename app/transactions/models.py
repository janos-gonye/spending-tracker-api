from datetime import datetime

from app.db import db


class Transaction(db.Model):
	__tablename__ = 'transactions'

	MIN_COMMENT_LEN = 0
	MAX_COMMENT_LEN = 300

	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Float, nullable=False) # amount of money, + -> income, - -> outcome
	processed_at = db.Column(db.DateTime, nullable=False) # when the money is earned or spent (stored as DateTime, it's useful when creating financial reports)
	comment = db.Column(db.String(MAX_COMMENT_LEN), default="")
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='cascade'), nullable=False)

	def as_dict(self):
		return {
			'id': self.id,
			'amount': self.amount,
			'processed_at': self.processed_at,
			'comment': self.comment,
			'category_id': self.category_id,
		}
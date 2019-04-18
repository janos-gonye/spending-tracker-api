from datetime import datetime

from app.db import db
from app.utils import datetime2timestamp


# TODO: find out how to add unique together constraint to the model (if possible) 
class Category(db.Model):
	"""user_id, title and parent_id must be unique together"""
	__tablename__ = 'categories'
	
	MIN_TITLE_LEN = 3
	MAX_TITLE_LEN = 50
	MIN_DESCRIPTION_LEN = 0
	MAX_DESCRIPTION_LEN = 120

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(MAX_TITLE_LEN), nullable=False)
	description = db.Column(db.String(MAX_DESCRIPTION_LEN), nullable=False, default='')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
	parent_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='cascade'), nullable=True, default=None)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	children = db.relationship("Category", cascade="all,delete")
	transactions = db.relationship("Transaction", cascade="all,delete")

	@property
	def parent(self):
		parent = Category.query.filter_by(id=self.parent_id).all()
		if len(parent) == 0:
			return None
		return parent[0]

	def as_dict(self):
		if not self.parent:
			parent = None
		else:
			parent = self.parent.as_dict()
		return {
			'id': self.id,
			'title': self.title,
			'description': self.description,
			'parent': parent,
			'created_at': datetime2timestamp(self.created_at),
			'updated_at': datetime2timestamp(self.updated_at),
		}

from app.db import db


"""
As you can see there is only one model called <Category>.
On the other hand in routes.py you can see categories and subcategories.

The reason of this
1, Later I might want to make it possible
   to add subcategories to other subcategories as many as one wishes.
2. It's seems to me that it is more logical this way
   than having <Category> and <Subcategory> models.

In routes.py category means <Category> model without a parent category
as subcategory means <Category> with a parent category.
"""
class Category(db.Model):	
	__tablename__ = 'categories';
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(120), nullable=False, default='')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
	parent_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='cascade'), nullable=True, default=None)
	children = db.relationship("Category")

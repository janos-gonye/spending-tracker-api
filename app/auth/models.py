from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	role = db.Column(db.String(20))
	password_hash = db.Column(db.String(255))

	def __init__(self, public_id, email, password, role='user'):
		"""roles: <user> and <admin>"""
		self.public_id = public_id
		self.email = email.lower()
		self.role = role.lower()
		self.set_password(password)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

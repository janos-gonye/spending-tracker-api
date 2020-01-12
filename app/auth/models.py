from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    categories = db.relationship('Category', cascade="all,delete")
    scheduled_transactions = db.relationship('ScheduledTransaction',
                                             cascade="all,delete")

    def __init__(self, public_id, email, password, role=10):
        """int role: <user: 10> and <admin: 90>"""
        self.public_id = public_id
        self.email = email.lower()
        self.role = role
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

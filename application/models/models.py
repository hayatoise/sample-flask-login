from datetime import datetime

from flask_login import UserMixin

from application.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    __table_args__ = (
        db.UniqueConstraint('name'),
        db.UniqueConstraint('email'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15, collation='utf8mb4_general_ci'), nullable=False)
    display_name = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    email = db.Column(db.String(256, collation='utf8mb4_general_ci'), nullable=False)
    password = db.Column(db.String(1024, collation='utf8mb4_general_ci'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, display_name, email, password):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = password

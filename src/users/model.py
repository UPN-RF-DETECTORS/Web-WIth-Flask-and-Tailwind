from datetime import datetime
from uuid import uuid4
# lokal
from core.db_config import db
from post.model import Post


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String, primary_key=True, default=uuid4)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
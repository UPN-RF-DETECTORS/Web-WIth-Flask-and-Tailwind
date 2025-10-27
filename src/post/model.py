from datetime import datetime
from uuid import uuid4

from core.db_config import db

class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.String, primary_key=True, default=lambda:str(uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    image_url = db.Column(db.String, nullable=False)
    result = db.Column(db.JSON, nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Post {self.post_id} by User {self.user_id}>"

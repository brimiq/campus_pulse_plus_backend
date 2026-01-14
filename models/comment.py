from app import db
from datetime import datetime


class Comment(db.Model):
   __tablename__ = 'comments'
   id = db.Column(db.Integer, primary_key=True)
   content = db.Column(db.String(150), nullable=False)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

from datetime import datetime
from marshmallow import Schema, fields, validate, ValidationError

from db import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(255), nullable=True)  # URL or path
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (assuming User and Category models exist)
    # user = db.relationship('User', backref='posts')
    # category = db.relationship('Category', backref='posts')

    def __repr__(self):
        return f'<Post {self.id}: {self.content[:20]}...>'

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=[
        validate.Length(min=1, max=500, error="Content must be between 1 and 500 characters")
    ])
    image = fields.Str(validate=validate.Length(max=255), allow_none=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
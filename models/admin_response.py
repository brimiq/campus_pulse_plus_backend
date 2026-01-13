from sqlalchemy.orm import relationship
from models.user import db

class AdminResponse(db.Model):
    __tablename__ = "admin_responses"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
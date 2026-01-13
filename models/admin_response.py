from config import db

class AdminResponse(db.Model):
    __tablename__ = "admin_responses"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id
        }


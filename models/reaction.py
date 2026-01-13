from config import db
from datetime import datetime

class Reaction(db.Model):
    __tablename__ = 'reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    reaction_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reactions')
    post = db.relationship('Post', backref='reactions')
    
    # Unique constraint: one reaction per user per post
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_reaction'),
    )
    
    def __repr__(self):
        return f'<Reaction {self.user_id} {self.reaction_type}d post {self.post_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'reaction_type': self.reaction_type,
            'created_at': self.created_at.isoformat()
        }
from flask import Blueprint, request, jsonify
from app import db
from models.comment import Comment


comment_bp = Blueprint("comment", __name__)




@comment_bp.route("/comments", methods=["POST"])
def add_comment():
   data = request.get_json()
  
  
   if not data or 'content' not in data:
    return jsonify({"error": "Comment content is required"}), 400


   new_comment = Comment(
       content=data["content"],
       post_id=data["post_id"]
   )
  
   db.session.add(new_comment)
   db.session.commit()


   return jsonify({"message": "Comment added!", "id": new_comment.id}), 201




@comment_bp.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id):
  
   comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
  
   output = []
   for c in comments:
       output.append({
           "id": c.id,
           "content": c.content,
           "created_at": c.created_at
       })
   return jsonify(output), 200
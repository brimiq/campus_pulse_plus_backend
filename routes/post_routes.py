from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import db
from models.post import Post, PostSchema

post_bp = Blueprint("post", __name__)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@post_bp.route("/posts", methods=["POST"])
def create_post():
    try:
        data = post_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400

    new_post = Post(
        content=data["content"],
        image=data.get("image"),
        user_id=data["user_id"],
        category_id=data["category_id"],
    )
    db.session.add(new_post)
    db.session.commit()

    return post_schema.dump(new_post), 201


@post_bp.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify(posts_schema.dump(posts)), 200


@post_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post_schema.dump(post), 200


@post_bp.route("/posts/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    try:
        data = post_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400

    for key, value in data.items():
        setattr(post, key, value)

    db.session.commit()
    return post_schema.dump(post), 200


@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200

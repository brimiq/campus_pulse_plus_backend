from flask import Blueprint, request, jsonify
from models.category import Category
from models.db import db

category_bp = Blueprint("categories", __name__, url_prefix="/categories")

# Create category
@category_bp.route("", methods=["POST"])
def create_category():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return {"error": "Category name required"}, 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({
        "id": category.id,
        "name": category.name
    }), 201


# Get all categories
@category_bp.route("", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([
        {"id": c.id, "name": c.name} for c in categories
    ])

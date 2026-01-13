from flask import Blueprint, request, session, jsonify
from models.user import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 400

    user = User(email=email, role="student")
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    session["role"] = user.role

    return user.to_dict(user), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return {"error": "Invalid credentials"}, 401

    session["user_id"] = user.id
    session["role"] = user.role

    return user.to_dict(user), 200

@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.clear()
    return {}, 204

@auth_bp.route("/me")
def me():
    if "user_id" not in session:
        return {}, 401

    user = User.query.get(session["user_id"])
    return user.to_dict(user), 200
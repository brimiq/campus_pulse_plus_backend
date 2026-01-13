from flask import Blueprint, request, session, jsonify
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    # ADMIN LOGIN
    if user and user.is_admin():
        if user.check_password(password):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid admin credentials"}, 401

    # STUDENT AUTO SIGNUP
    if not user:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    if user.check_password(password):
        session["user_id"] = user.id
        return user.to_dict(), 200

    return {"error": "Invalid credentials"}, 401


@auth_bp.route("/me")
def me():
    user = User.query.get(session.get("user_id"))
    return user.to_dict() if user else {}, 200


@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.clear()
    return {}, 204

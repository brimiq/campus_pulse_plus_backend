from flask import Blueprint, request, session, jsonify
from models.user import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    pass

@auth_bp.route("/login", methods=["POST"])
def login():
    pass

@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    pass

@auth_bp.route("/me")
def me():
    pass
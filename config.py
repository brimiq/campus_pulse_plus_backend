from flask import Blueprint, request, session
from models import db, User, AdminResponse

admin_bp = Blueprint("admin", __name__)

def admin_required():
    user = User.query.get(session.get("user_id"))
    return user and user.is_admin()

@admin_bp.route("/admin/responses", methods=["POST"])
def create_admin_response():
    if not admin_required():
        return {"error": "Admin only"}, 403

    data = request.get_json()

    response = AdminResponse(
        content=data["content"],
        post_id=data["post_id"],
        admin_id=session["user_id"]
    )

    db.session.add(response)
    db.session.commit()

    return response.to_dict(), 201

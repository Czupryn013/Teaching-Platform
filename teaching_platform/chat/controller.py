from flask import Blueprint, render_template

from teaching_platform.models.extensions import auth

chat_controller_bp = Blueprint("chat_controller_bp", __name__)


@chat_controller_bp.route("/chat", methods=["GET"])
@auth.login_required()
# @auth.login_required(role=[Role.ADMIN, Role.TEACHER, Role.STUDENT])
def chat():
    user = auth.current_user()
    return render_template("chat.html", username=user.username)
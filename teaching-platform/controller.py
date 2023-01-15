from flask import Blueprint
from flask import request

from extensions import auth
from models import Role
import db_handler
import exceptions


controller_bp = Blueprint("controller_bp", __name__)


@auth.verify_password
def verify_password(username, password):
    try:
        user = db_handler.check_auth(username, password)
    except exceptions.AuthError:
        return None
    return user

@auth.get_user_roles
def get_user_roles(user):
    return user.role


@controller_bp.route("/users", methods=["POST"])
def add_user():
    try:
        request_data = request.get_json()
        username, password = request_data.get("username"), request_data.get("password")

        if not username or not password: return "Incorrect json body", 400
        db_handler.add_user(username, password)
        return f"User {username} has been added sucessfuly.", 201
    except (exceptions.UsernameTakenError,exceptions.PasswordToWeakError,exceptions.IncorrectUsername) as e:
        return e.message, e.status

@controller_bp.route("/users/<id_to_delete>", methods=["DELETE"])
@auth.login_required(role=Role.ADMIN.value)
def remove_user(id_to_delete):
    try:
        db_handler.remove_user(id_to_delete)
        return f"User with id {id_to_delete} has been deleted sucessfuly.", 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@controller_bp.route("/users", methods=["GET"])
@auth.login_required(role=Role.ADMIN.value)
def see_all_users():
    return db_handler.see_all_users(), 200

@controller_bp.route("/users/me", methods=["GET"])
@auth.login_required()
def see_user_data():
    user_id = auth.current_user().id
    try:
        results = db_handler.see_user_data(user_id)
        return results, 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status



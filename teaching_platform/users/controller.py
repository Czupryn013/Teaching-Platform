from flask import Blueprint, request

from teaching_platform.extensions import auth
from teaching_platform.models import Role, get_all_roles
from teaching_platform.users import db_handler, exceptions

user_controller_bp = Blueprint("user_controller_bp", __name__)

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


@user_controller_bp.route("/users", methods=["POST"])
def add_user():
    request_data = request.get_json()
    username, password = request_data.get("username"), request_data.get("password")

    if not username or not password: return "Incorrect json body", 400

    try:
        db_handler.add_user(username, password)
    except exceptions.UserCredentialsError as e:
        return e.message, e.status

    return f"User {username} has been added sucessfuly.", 201

@user_controller_bp.route("/users/<id_to_delete>", methods=["DELETE"])
@auth.login_required(role=Role.ADMIN)
def remove_user(id_to_delete):
    try:
        db_handler.remove_user(id_to_delete)
        return f"User with id {id_to_delete} has been deleted sucessfuly.", 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@user_controller_bp.route("/users", methods=["GET"])
@auth.login_required()
def get_all_users():
    results, users = db_handler.get_all_users(), []
    for user in results: users.append(user.get_censured_json())

    return users, 200

@user_controller_bp.route("/users/<user_id>", methods=["GET"])
@auth.login_required(role=Role.ADMIN)
def get_user(user_id):
    try:
        results = db_handler.get_user(user_id).get_censured_json()
        return results, 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@user_controller_bp.route("/users/me", methods=["GET"])
@auth.login_required()
def get_my_data():
    user_id = auth.current_user().id
    try:
        results = db_handler.get_user(user_id).get_censured_json()
        return results, 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@user_controller_bp.route("/users/me", methods=["PATCH"])
@auth.login_required()
def update_my_info():
    request_data = request.get_json()
    current_id = auth.current_user().id
    username, password = request_data.get("username"), request_data.get("password")
    if not username and not password: return "Incorrect json body", 400

    if username:
        try:
            db_handler.update_username(username, current_id)
        except exceptions.UserDosentExistError as e:
            return e.message, e.status
    elif password:
        try:
            db_handler.update_password(password, current_id)
        except (exceptions.UserDosentExistError, exceptions.UserCredentialsError) as e:
            return e.message, e.status

    return "Patched sucesfully!", 200

@user_controller_bp.route("/users/<user_id>", methods=["PATCH"])
@auth.login_required(role=Role.ADMIN)
def change_user_role(user_id):
    request_data = request.get_json()
    role = request_data.get("role")
    if not role: return "Incorrect json body", 400
    elif role not in get_all_roles(): return "Incorrect role value.", 400

    try:
        db_handler.update_role(role, user_id)
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

    return f"Role of user with id {user_id} changed to {role} sucesfully!"
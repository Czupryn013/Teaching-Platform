import logging
import smtplib

from flask import Blueprint, request

from teaching_platform.models.extensions import auth
from teaching_platform.models.models import Role, get_all_roles
from teaching_platform.models.users import db_handler, exceptions
from teaching_platform.models.users.token import confirm_token, generate_confirmation_token, send_email

user_controller_bp = Blueprint("user_controller_bp", __name__)

@auth.verify_password
def verify_password(username, password):
    try:
        user = db_handler.check_auth(username, password)
    except exceptions.AuthError as e:
        logging.warning(e.message)
        return None
    return user

@auth.get_user_roles
def get_user_roles(user):
    return user.role


@user_controller_bp.route("/users", methods=["POST"])
def add_user():
    request_data = request.get_json()
    username, password, email = request_data.get("username"), request_data.get("password"), request_data.get("email")

    if not all((username, password, email)): return "Incorrect json body", 400

    try:
        db_handler.add_user(username, password, email)
    except exceptions.UserCredentialsError as e:
        logging.warning(e.message)
        return e.message, e.status

    token = generate_confirmation_token(email)
    try:
        send_email(email, f"Confirmation Email for {username}", f"Click here to confirm! -> http://127.0.0.1:5000/users/confirm/{token}")
    except smtplib.SMTPAuthenticationError:
        return "Failed to send an verification e-mail. Incorrect logging data.", 400

    return f"Email to {username} has been sent sucessfuly.", 201

@user_controller_bp.route("/users/<id_to_delete>", methods=["DELETE"])
@auth.login_required(role=Role.ADMIN)
def remove_user(id_to_delete):
    try:
        db_handler.remove_user(id_to_delete)
        return f"User with id {id_to_delete} has been deleted sucessfuly.", 200
    except exceptions.UserDosentExistError as e:
        logging.warning(e.message)
        return e.message, e.status

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
        logging.warning(e.message)
        return e.message, e.status

    return f"Role of user with id {user_id} changed to {role} sucesfully!"

@user_controller_bp.route("/users", methods=["GET"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER, Role.STUDENT])
def get_all_users():
    results, users = db_handler.get_all_users(), []
    for user in results: users.append(user.get_censured_json())

    return users, 200

@user_controller_bp.route("/users/<user_id>", methods=["GET"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER, Role.STUDENT])
def get_user(user_id):
    try:
        results = db_handler.get_user(user_id).get_censured_json()
        return results, 200
    except exceptions.UserDosentExistError as e:
        logging.warning(e.message)
        return e.message, e.status

@user_controller_bp.route("/users/me", methods=["GET"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER, Role.STUDENT])
def get_my_data():
    user_id = auth.current_user().id
    try:
        results = db_handler.get_user(user_id).get_censured_json()
        return results, 200
    except exceptions.UserDosentExistError as e:
        logging.warning(e.message)
        return e.message, e.status

@user_controller_bp.route("/users/me", methods=["PATCH"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER, Role.STUDENT])
def update_my_info():
    request_data = request.get_json()
    current_id = auth.current_user().id
    username, password = request_data.get("username"), request_data.get("password")
    if not username and not password: return "Incorrect json body", 400

    if username:
        try:
            db_handler.update_username(username, current_id)
        except exceptions.UserDosentExistError as e:
            logging.warning(e.message)
            return e.message, e.status
    elif password:
        try:
            db_handler.update_password(password, current_id)
        except (exceptions.UserDosentExistError, exceptions.UserCredentialsError) as e:
            logging.warning(e.message)
            return e.message, e.status

    return "Patched sucesfully!", 200

@user_controller_bp.route("/users/password", methods=["POST"])
def reset_password():
    request_data = request.get_json()
    email = request_data.get("email")
    if not email: return "Incorrect json body", 400

    try:
        user = db_handler.get_user_by_email(email)
    except exceptions.UserDosentExistError as e:
        return e.message, e.status


    token = generate_confirmation_token(user.email)
    send_email(user.email, f"Reset Password Email for {user.username}",
               f"Click here to reset your password! -> http://127.0.0.1:5000/users/password/{token}")

    return f"Reset password email to {user.username} has been sent sucessfully.", 201

@user_controller_bp.route("/users/password/<token>", methods=["POST"])
def confirm_reset_password(token):
    request_data, email = request.get_json(),confirm_token(token)

    new_password = request_data.get("new_password")
    if not new_password: return "Incorrect json body", 400
    try:
        user = db_handler.get_user_by_email(email)
    except exceptions.UserDosentExistError as e:
        return e.message, e.status


    try:
        db_handler.update_password(new_password, user.id)
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

    return "Password has been changed sucesfully!", 200

@user_controller_bp.route('/users/confirm/<token>', methods=["GET"])
@auth.login_required()
def confirm_email(token):
    email = confirm_token(token)

    user = auth.current_user()

    if user.email != email:
        logging.info("Authorization failure.")
        return "Authorization failure.", 401

    if user.role != Role.UNCOMFIRMED:
        logging.info("Account already confirmed.")
        return "Account already confirmed.", 200
    else:
        db_handler.update_role(Role.STUDENT, user.id)
        logging.info("Account sucesfuly confirmed.")
        return "Account sucesfuly confirmed.", 200

@user_controller_bp.route('/users/confirm', methods=["GET"])
@auth.login_required()
def resend_confirmation_email():
    user = auth.current_user()

    if user.role != Role.UNCOMFIRMED:
        logging.info("Account already confirmed.")
        return "Account already confirmed.", 200

    token = generate_confirmation_token(user.email)
    send_email(user.email, f"Confirmation Email for {user.username}", f"Click here to confirm! -> http://127.0.0.1:5000/users/confirm/{token}")

    logging.info(f"Confirmation email to {user.username} has been resend sucessfuly.")

    return f"Confirmation email to {user.username} has been resend sucessfuly.", 201
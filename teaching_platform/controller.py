from flask import Blueprint, request

from teaching_platform.extensions import auth
from teaching_platform.models import Role, get_all_roles
from teaching_platform.users import db_handler as user_db_handler, exceptions
from teaching_platform.lessons import db_handler as lesson_db_handler, exceptions as l_exceptions

controller_bp = Blueprint("controller_bp", __name__)


@auth.verify_password
def verify_password(username, password):
    try:
        user = user_db_handler.check_auth(username, password)
    except exceptions.AuthError:
        return None
    return user

@auth.get_user_roles
def get_user_roles(user):
    return user.role

@controller_bp.route("/users", methods=["POST"])
def add_user():
    request_data = request.get_json()
    username, password = request_data.get("username"), request_data.get("password")

    if not username or not password: return "Incorrect json body", 400

    try:
        user_db_handler.add_user(username, password)
    except exceptions.UserCredentialsError as e:
        return e.message, e.status

    return f"User {username} has been added sucessfuly.", 201

@controller_bp.route("/users/<id_to_delete>", methods=["DELETE"])
@auth.login_required(role=Role.ADMIN)
def remove_user(id_to_delete):
    try:
        user_db_handler.remove_user(id_to_delete)
        return f"User with id {id_to_delete} has been deleted sucessfuly.", 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@controller_bp.route("/users", methods=["GET"])
@auth.login_required()
def get_all_users():
    return user_db_handler.get_all_users(), 200

@controller_bp.route("/users/<user_id>", methods=["GET"])
@auth.login_required(role=Role.ADMIN)
def get_user_data(user_id):
    try:
        results = user_db_handler.get_user_data(user_id)
        return results, 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@controller_bp.route("/users/me", methods=["GET"])
@auth.login_required()
def get_my_data():
    user_id = auth.current_user().id
    try:
        results = user_db_handler.get_user_data(user_id)
        return results, 200
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

@controller_bp.route("/users/me", methods=["PATCH"])
@auth.login_required()
def update_my_info():
    request_data = request.get_json()
    current_id = auth.current_user().id
    username, password = request_data.get("username"), request_data.get("password")
    if not username and not password: return "Incorrect json body", 400

    if username:
        try:
            user_db_handler.update_username(username, current_id)
        except exceptions.UserDosentExistError as e:
            return e.message, e.status
    elif password:
        try:
            user_db_handler.update_password(password, current_id)
        except (exceptions.UserDosentExistError, exceptions.UserCredentialsError) as e:
            return e.message, e.status

    return "Patched sucesfully!", 200

@controller_bp.route("/update/<user_id>", methods=["PATCH"])
@auth.login_required(role=Role.ADMIN)
def change_user_role(user_id):
    request_data = request.get_json()
    role = request_data.get("role")
    if not role: return "Incorrect json body", 400
    elif role not in get_all_roles(): return "Incorrect role value.", 400

    try:
        user_db_handler.update_role(role, user_id)
    except exceptions.UserDosentExistError as e:
        return e.message, e.status

    return f"Role of user with id {user_id} changed to {role} sucesfully!"



@controller_bp.route("/lessons", methods=["POST"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def add_lesson():
    request_data = request.get_json()
    teacher_id, info = request_data.get("teacher_id"), request_data.get("info")

    if not teacher_id or not info: return "Incorrect json body.", 400

    try:
        lesson_db_handler.add_lesson(teacher_id, info)
    except l_exceptions.ResourceDosentExistError as e:
        return e.message, e.status

    return f"Lesson with teacher {teacher_id} has been added sucessfuly.", 201

@controller_bp.route("/lessons/<lesson_id>/add", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def add_student_to_lesson(lesson_id):
    request_data = request.get_json()
    student_id = request_data.get("student_id")
    teacher_id = auth.current_user().id
    if not student_id: return "Incorrect json body", 400

    try:
        lesson_db_handler.add_student_to_lesson(student_id, lesson_id, teacher_id)
    except (l_exceptions.UserAlreadyAddedError, l_exceptions.AuthError) as e:
        return e.message, e.status

    return f"User {student_id} added to lesson {lesson_id} sucesfully!"

@controller_bp.route("/lessons", methods=["GET"])
@auth.login_required()
def get_all_lessons():
    return lesson_db_handler.get_all_lessons(), 200

@controller_bp.route("/lessons/<lesson_id>", methods=["GET"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def get_lesson(lesson_id):
    try:
        results = lesson_db_handler.get_lesson(lesson_id)
    except l_exceptions.LessonDosentExistError as e:
        return e.message, e.status
    return results, 200


@controller_bp.route("/lessons/<lesson_id>", methods=["DELETE"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def remove_lesson(lesson_id):
    teacher_id = auth.current_user().id
    try:
        lesson_db_handler.remove_lesson(lesson_id, teacher_id)
        return f"Lesson with id {lesson_id} has been deleted sucessfuly.", 200
    except (l_exceptions.LessonDosentExistError, l_exceptions.AuthError) as e:
        return e.message, e.status

@controller_bp.route("/lessons/<lesson_id>", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def update_lesson_details(lesson_id):
    request_data, teacher_id = request.get_json(), auth.current_user().id
    pre_lesson, info, homework = request_data.get("pre_lesson"), request_data.get("info"), request_data.get("homework")
    if not [pre_lesson,info, homework]: return "Incorrect json bodyaa", 400


    try:
        lesson_db_handler.update_lesson_details(lesson_id, teacher_id, request_data)
    except (l_exceptions.LessonDosentExistError, l_exceptions.AuthError) as e:
        return e.message, e.status

    return "Patched sucesfully!", 200
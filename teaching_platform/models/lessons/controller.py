import logging

from flask import Blueprint, request

from teaching_platform.models.extensions import auth
from teaching_platform.models.models import Role
from teaching_platform.models.lessons import db_handler, exceptions
from teaching_platform.models import validation
lesson_controller_bp = Blueprint("lesson_controller_bp", __name__)

@lesson_controller_bp.route("/lessons", methods=["POST"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def add_lesson():
    request_data = request.get_json()
    teacher_id, info = request_data.get("teacher_id"), request_data.get("info")

    if not teacher_id or not info: return "Incorrect json body.", 400

    try:
        db_handler.add_lesson(teacher_id, info)
    except exceptions.ResourceDosentExistError as e:
        logging.warning(e.message)
        return e.message, e.status

    return f"Lesson with teacher {teacher_id} has been added sucessfuly.", 201

@lesson_controller_bp.route("/lessons/<lesson_id>/add", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def add_student_to_lesson(lesson_id):
    request_data = request.get_json()
    student_id = request_data.get("student_id")
    teacher_id = auth.current_user().id
    if not student_id: return "Incorrect json body", 400

    try:
        validation.validate_teacher(teacher_id, lesson_id)
        db_handler.add_student_to_lesson(student_id, lesson_id)
    except (exceptions.ResourceDosentExistError, exceptions.AuthError) as e:
        logging.warning(e.message)
        return e.message, e.status

    return f"User {student_id} added to lesson {lesson_id} sucesfully!"

@lesson_controller_bp.route("/lessons/<lesson_id>/remove", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def remove_student_from_lesson(lesson_id):
    request_data = request.get_json()
    student_id, teacher_id = request_data.get("student_id"), auth.current_user().id
    if not student_id: return "Incorrect json body", 400

    try:
        validation.validate_teacher(teacher_id, lesson_id)
        db_handler.remove_student_from_lesson(student_id, lesson_id)
    except (exceptions.ResourceDosentExistError, exceptions.AuthError) as e:
        logging.warning(e.message)
        return e.message, e.status

    return f"User {student_id} has been removed from lesson {lesson_id} sucesfully!"

@lesson_controller_bp.route("/lessons", methods=["GET"])
@auth.login_required()
def get_all_lessons():
    results, lessons = db_handler.get_all_lessons(), []
    for lesson in results: lessons.append(lesson.get_json())
    return lessons, 200

@lesson_controller_bp.route("/lessons/<lesson_id>", methods=["GET"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def get_lesson(lesson_id):
    try:
        results = db_handler.get_lesson(lesson_id).get_json()
    except exceptions.LessonDosentExistError as e:
        logging.warning(e.message)
        return e.message, e.status
    return results, 200


@lesson_controller_bp.route("/lessons/<lesson_id>", methods=["DELETE"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def remove_lesson(lesson_id):
    teacher_id = auth.current_user().id
    try:
        validation.validate_teacher(teacher_id, lesson_id)
        db_handler.remove_lesson(lesson_id)
    except (exceptions.LessonDosentExistError, exceptions.AuthError) as e:
        logging.warning(e.message)
        return e.message, e.status

    return f"Lesson with id {lesson_id} has been deleted sucessfuly.", 200

@lesson_controller_bp.route("/lessons/<lesson_id>", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def update_lesson_details(lesson_id):
    request_data, teacher_id = request.get_json(), auth.current_user().id
    pre_lesson, info, homework = request_data.get("pre_lesson"), request_data.get("info"), request_data.get("homework")
    if not [pre_lesson,info, homework]: return "Incorrect json body", 400


    try:
        db_handler.update_lesson_details(lesson_id, request_data)
    except (exceptions.LessonDosentExistError, exceptions.AuthError) as e:
        logging.warning(e.message)
        return e.message, e.status

    return "Patched sucesfully!", 200
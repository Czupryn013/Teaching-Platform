from flask import Blueprint, request

from teaching_platform.extensions import auth
from teaching_platform.models import Role
from teaching_platform.projects import db_handler, exceptions
from teaching_platform import validation

project_controller_bp = Blueprint("project_controller_bp", __name__)


@project_controller_bp.route("/projects", methods=["POST"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def add_project():
    request_data = request.get_json()
    mentor_id, name = request_data.get("mentor_id"), request_data.get("name")

    if not name or not mentor_id: return "Incorrect json body.", 400

    try:
        db_handler.add_project(name, mentor_id)
    except exceptions.ResourceDosentExistError as e:
        return e.message, e.status

    return f"Project {name} with mentor {mentor_id} has been added sucessfuly.", 201

@project_controller_bp.route("/projects", methods=["GET"])
@auth.login_required()
def get_all_projects():
    results, projects = db_handler.get_all_projects(), []
    for result in results: projects.append(result.get_json())
    return projects

@project_controller_bp.route("/projects/<project_id>", methods=["GET"])
@auth.login_required()
def get_project(project_id):
    try:
        project = db_handler.get_project(project_id)
    except exceptions.ProjectDosentExistError as e:
        return e.message, e.status
    return project.get_json(), 200

@project_controller_bp.route("/projects/<project_id>", methods=["DELETE"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def remove_project(project_id):
    mentor_id = auth.current_user().id
    try:
        validation.validate_mentor(mentor_id, project_id)
        db_handler.remove_project(project_id)
    except (exceptions.ProjectDosentExistError, exceptions.AuthError) as e:
        return e.message, e.status

    return f"Project with id {project_id} has been deleted sucessfuly.", 200

@project_controller_bp.route("/projects/<project_id>", methods=["PATCH"])
@auth.login_required(role=[Role.ADMIN, Role.TEACHER])
def update_proejct(project_id):
    request_data = request.get_json()
    mentor_id = auth.current_user().id
    status, info, name = request_data.get("status"),  request_data.get("info"),  request_data.get("name")
    if not [status, info, name]: return "Incorrect json body", 400

    try:
        validation.validate_mentor(mentor_id, project_id)
        db_handler.update_project(project_id, request_data)
    except exceptions.ProjectDosentExistError as e:
        return e.message, e.status

    return "Patched sucesfully!", 200

@project_controller_bp.route("/projects/<project_id>/mentor", methods=["PATCH"])
@auth.login_required(role=Role.ADMIN)
def reasign_mentor(project_id):
    request_data = request.get_json()
    new_mentor_id = request_data.get("mentor_id")
    mentor_id = auth.current_user().id
    if not mentor_id: return "Incorrect json body", 400

    try:
        validation.validate_mentor(mentor_id, project_id)
        db_handler.reasign_mentor(project_id, new_mentor_id)
    except (exceptions.ProjectDosentExistError, exceptions.MentorDosentExistError) as e:
        return e.message, e.status

    return "Reasigned sucesfully!", 200

@project_controller_bp.route("/projects/<project_id>/add", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def add_user_to_project(project_id):
    request_data = request.get_json()
    user_id = request_data.get("student_id")
    mentor_id = auth.current_user().id
    if not user_id: return "Incorrect json body", 400

    try:
        validation.validate_mentor(mentor_id, project_id)
        db_handler.add_user_to_project(user_id, project_id)
    except exceptions.ResourceDosentExistError as e:
        return e.message, e.status

    return f"User {user_id} has been added to project {project_id} sucesfully!"

@project_controller_bp.route("/projects/<project_id>/remove", methods=["PATCH"])
@auth.login_required(role = [Role.ADMIN, Role.TEACHER])
def remove_user_from_project(project_id):
    request_data = request.get_json()
    user_id = request_data.get("student_id")
    mentor_id = auth.current_user().id
    if not user_id: return "Incorrect json body", 400

    try:
        validation.validate_mentor(mentor_id, project_id)
        db_handler.remove_user_from_project(user_id, project_id)
    except exceptions.ResourceDosentExistError as e:
        return e.message, e.status

    return f"User {user_id} has been removed from project {project_id} sucesfully!"
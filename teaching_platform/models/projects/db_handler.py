import logging

from teaching_platform.models.projects import exceptions
from teaching_platform.models.models import User, Role, Project
from teaching_platform.models.extensions import db

def add_project(name, mentor_id, status="In development."):
    mentor = User.query.filter_by(id=mentor_id, role=Role.TEACHER).first()
    if not mentor: raise exceptions.MentorDosentExistError()
    project = Project(mentor=mentor, name=name, status=status)

    db.session.add(project)
    db.session.commit()

def get_all_projects():
    return Project.query.all()

def get_project(project_id):
    project = Project.query.filter_by(id = project_id).first()
    if not project: raise exceptions.ProjectDosentExistError()

    return project

def remove_project(project_id):
    query = Project.query.filter_by(id=project_id)
    project = query.first()
    if not project: raise exceptions.ProjectDosentExistError()

    project.students = []
    query.delete()
    db.session.commit()

    logging.info(f"User with id {project_id} has been removed sucessfuly.")

def update_project(project_id, updates):
    project = Project.query.filter_by(id=project_id).first()
    if not project: raise exceptions.ProjectDosentExistError()

    status, info, name = updates.get("status"), updates.get("info"), updates.get("name")

    if status: project.status = status
    if info: project.info = info
    if name: project.name = name
    db.session.commit()

def reasign_mentor(project_id, mentor_id):
    project, mentor = Project.query.filter_by(id=project_id).first(), User.query.filter_by(id=mentor_id, role=Role.TEACHER).first()
    if not project: raise exceptions.ProjectDosentExistError()
    if not mentor: raise exceptions.MentorDosentExistError()

    project.mentor = mentor
    db.session.commit()


def add_user_to_project(student_id, project_id):
    project = Project.query.filter_by(id=project_id).first()
    user = User.query.filter_by(id=student_id).first()

    if not user: raise exceptions.UserDosentExistError()
    if not project: raise exceptions.ProjectDosentExistError()


    project.students.append(user)
    db.session.commit()

def remove_user_from_project(student_id, project_id):
    project = Project.query.filter_by(id=project_id).first()
    user = User.query.filter_by(id=student_id).first()

    if not user: raise exceptions.UserDosentExistError()
    if not project: raise exceptions.ProjectDosentExistError()


    project.students.remove(user)
    db.session.commit()

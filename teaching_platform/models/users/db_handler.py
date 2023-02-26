import logging

from werkzeug.security import check_password_hash

from teaching_platform.models.models import User, Role
from teaching_platform.models.extensions import db
from teaching_platform.models.users import exceptions
from teaching_platform.models import validation


def add_user(username, password, email):
    validation.validate_username(username)
    encoded_password = validation.validate_password(password)

    user = User(username=username, password=encoded_password, email=email, role=Role.UNCOMFIRMED)

    results = User.query.filter_by(username=username).all()
    results2 = User.query.filter_by(email=email).all()
    if results: raise exceptions.UsernameTakenError()
    if results2: raise exceptions.EmailTakenError()


    db.session.add(user)
    db.session.commit()

    logging.info(f"User {username} added")

def remove_user(id_to_delete):
    query = User.query.filter_by(id=id_to_delete)
    user = query.first()

    if not user: raise exceptions.UserDosentExistError()

    user.lessons = []
    query.delete()
    db.session.commit()

    logging.info(f"User with id {id_to_delete} has been removed sucessfuly.")

def get_all_users():
    results = User.query.all()

    return results

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user: raise exceptions.UserDosentExistError()

    return user

def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if not user: raise exceptions.UserDosentExistError()

    return user

def check_auth(username, password):
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password): return user

    raise exceptions.AuthError()

def update_username(username, id):
    user = User.query.filter_by(id=id).first()
    if not user: raise exceptions.UserDosentExistError()

    validation.validate_username(username)

    user.username = username
    db.session.commit()

def update_role(role, id):
    user = User.query.filter_by(id=id).first()
    if not user: raise exceptions.UserDosentExistError()

    user.role = role
    db.session.commit()

def update_password(password, id):
    user = User.query.filter_by(id=id).first()
    if not user: raise exceptions.UserDosentExistError()

    encoded_password = validation.validate_password(password)

    user.password = encoded_password
    db.session.commit()
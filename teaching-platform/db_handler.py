import logging

import yaml
import jsonpickle
from werkzeug.security import check_password_hash
from sqlalchemy.orm import load_only
from flask.json import jsonify

import exceptions
from models import User, Role
from extensions import db
import validation


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

logging.basicConfig(level=logging.INFO, filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

def add_user(username, password):
    username = validation.validate_username(username)
    encoded_password = validation.validate_password(password)

    user = User(username=username, password=encoded_password, role=Role.STUDENT)

    results = User.query.filter_by(username=username).all()
    if results: raise exceptions.UsernameTakenError()

    db.session.add(user)
    db.session.commit()

    logging.info(f"User {username} added")

def remove_user(id_to_delete):
    query = User.query.filter_by(id=id_to_delete)
    user = query.first()

    if not user: raise exceptions.UserDosentExistError()

    query.delete()
    db.session.commit()

    logging.info(f"User with id {id_to_delete} has been removed sucessfuly.")

def see_all_users():
    results = User.query.all()
    users = []
    for user in results: users.append(user.get_censured_json())

    return users


def see_user_data(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user: raise exceptions.UserDosentExistError()


    return user.get_censured_json()

def check_auth(username, password):
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password): return user

    raise exceptions.AuthError()

def update_username(username, id):
    user = User.query.filter_by(id=id).first()
    if not user: raise exceptions.UserDosentExistError()

    username = validation.validate_username(username)

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



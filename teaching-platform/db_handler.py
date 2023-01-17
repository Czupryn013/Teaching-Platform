import logging

import yaml
import jsonpickle
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash

import exceptions
from models import User, CensuredUser, Role
from extensions import db


with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

policy = PasswordPolicy.from_names(length=5,uppercase=1, numbers=2,special=1, nonletters=2)

logging.basicConfig(level=logging.INFO,filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

def add_user(username, password):
    test = policy.test(password)

    if test: raise exceptions.PasswordToWeakError(f"Password breaks the following rules {test}.")
    if not username or " " in username or len(username) > 89: raise exceptions.IncorrectUsername()

    encoded_password = generate_password_hash(password, method="sha256")

    user = User(username=username, password=encoded_password, role=Role.STUDENT.value)

    results = User.query.filter_by(username=username).all()
    if results: raise exceptions.UsernameTakenError()

    db.session.add(user)
    db.session.commit()

    logging.info(f"User {username} added")

def remove_user(id_to_delete):
    results = User.query.filter_by(id=id_to_delete).first()

    if not results: raise exceptions.UserDosentExistError()

    User.query.filter_by(id=id_to_delete).delete()
    db.session.commit()

    logging.info(f"User with id {id_to_delete} has been removed sucessfuly.")

def see_all_users():
    results = User.query.all()
    users = []
    for user in results: users.append(CensuredUser(user.id, user.username, user.role))

    return jsonpickle.encode(users, unpicklable=False)

def see_user_data(user_id):
    results = User.query.filter_by(id=user_id).first()

    if not results: raise exceptions.UserDosentExistError()

    user = CensuredUser(results.id, results.username, results.role)

    return jsonpickle.encode(user, unpicklable=False)

def check_auth(username, password):
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password): return user

    raise exceptions.AuthError()

def update_username(username, id):
    user = User.query.filter_by(id=id).first()
    if not user: raise exceptions.UserDosentExistError()

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

    test = policy.test(password)

    if test: raise exceptions.PasswordToWeakError(f"Password breaks the following rules {test}.")

    encoded_password = generate_password_hash(password, method="sha256")

    user.password = encoded_password
    db.session.commit()



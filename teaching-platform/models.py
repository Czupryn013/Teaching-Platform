from enum import Enum

from extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable= False)
    password = db.Column(db.String(90),nullable= False)
    role = db.Column(db.String(20),nullable= False)

    def __repr__(self):
        return f"User(id: {self.id}, username: {self.username}, role: {self.role})"


#this model is needed for showing only public data not personal informations like password, for exaple in see_all_users()
class CensuredUser:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

#STUDENT, TEACHER, ADMIN
def get_all_roles():
    return ["STUDENT", "TEACHER", "ADMIN"]


class Role(Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"

    def __str__(self):
        return str(self.value)


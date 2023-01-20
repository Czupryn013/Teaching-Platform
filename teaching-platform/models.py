from enum import Enum

from extensions import db

class Role(Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"

    def __repr__(self):
        return str(self.value)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable= False)
    password = db.Column(db.String(),nullable= False)
    role = db.Column(db.Enum(Role),nullable= False)

    def __repr__(self):
        return f"User(id: {self.id}, username: {self.username}, role: {self.role})"

    def get_censured_json(self):
        return {"id": self.id, "username": self.username, "role": self.role.name}

    def get_json(self):
        return {"id": self.id, "username": self.username, "password": self.password, "role": self.role.name}


def get_all_roles():
    return [role.value for role in Role]



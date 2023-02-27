import yaml
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash

from tp_models.users import exceptions
from tp_models.users import db_handler as user_dbh
from tp_models.lessons import db_handler as lesson_dbh
from tp_models.projects import db_handler as project_dbh
from tp_models.models import Role

with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
pwd_config = config["password"]


def validate_password(password):
    policy = PasswordPolicy.from_names(length=pwd_config["length"], uppercase=pwd_config["uppercase"], numbers=pwd_config["numbers"],
                                       special=pwd_config["special"], nonletters=pwd_config["nonletters"])
    test = policy.test(password)

    if test: raise exceptions.PasswordToWeakError(f"Password breaks the following rules {test}.")

    return generate_password_hash(password, method="sha256")

def validate_username(username):
    if not username or " " in username or len(username) > 20: raise exceptions.IncorrectUsername()

def validate_teacher(teacher_id, lesson_id):
    teacher = user_dbh.get_user(teacher_id)
    lesson = lesson_dbh.get_lesson(lesson_id)

    if teacher.role != Role.ADMIN and lesson not in teacher.teaching: raise exceptions.AuthError()

def validate_mentor(mentor_id, project_id):
    teacher = user_dbh.get_user(mentor_id)
    project = project_dbh.get_project(project_id)

    if teacher.role != Role.ADMIN and project not in teacher.mentoring: raise exceptions.AuthError()
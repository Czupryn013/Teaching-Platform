from enum import Enum

from teaching_platform.extensions import db


class Role(Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    UNCOMFIRMED = "UNCOMFIRMED"
    ADMIN = "ADMIN"

    def __repr__(self):
        return str(self.value)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable= False)
    email = db.Column(db.String(100), unique=True, nullable= False)
    password = db.Column(db.String(),nullable= False)
    role = db.Column(db.Enum(Role),nullable= False)

    teaching = db.relationship("Lesson", backref="teacher")
    mentoring = db.relationship("Project", backref="mentor")

    def __repr__(self):
        return f"User(id: {self.id}, username: {self.username}, role: {self.role})"

    def get_censured_json(self):
        return {"id": self.id, "username": self.username, "role": self.role.name}

    def get_json(self):
        return {"id": self.id, "username": self.username, "password": self.password, "role": self.role.name}


def get_all_roles():
    print([role.value for role in Role])
    return [role.value for role in Role]


user_lessons = db.Table("user_lessons",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("lesson_id", db.Integer, db.ForeignKey("lessons.id"))
)

user_projects = db.Table("user_projects",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id"))
)

class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    students = db.relationship("User", secondary=user_lessons, backref="lessons")
    pre_lesson = db.Column(db.String())
    info = db.Column(db.String(), nullable=False)
    homework = db.Column(db.String())

    def get_json(self):
        all_students = []
        for student in self.students: all_students.append(student.username)
        return {"id": self.id, "teacher_id": self.teacher_id, "teacher": self.teacher.username, "info": self.info,"students": all_students}

    def get_censured_json(self):
        return {"teacher":self.teacher.username, "info": self.info}


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    students = db.relationship("User", secondary=user_projects, backref="projects")
    info = db.Column(db.String())
    status = db.Column(db.String(), nullable=False)


    def get_json(self):
        all_students = []
        for student in self.students: all_students.append(student.username)
        return {"id": self.id, "name": self.name, "mentor_id": self.mentor_id, "info": self.info, "status": self.status, "students": all_students}
import logging

from teaching_platform.models.lessons import exceptions
from teaching_platform.models.models import User, Role, Lesson
from teaching_platform.models.extensions import db


def add_lesson(teacher_id, info):
    teacher = User.query.filter_by(id=teacher_id, role=Role.TEACHER).first()
    if not teacher: raise exceptions.TeacherDosentExistError()
    lesson = Lesson(info=info, teacher=teacher)

    db.session.add(lesson)
    db.session.commit()

def add_student_to_lesson(student_id, lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    student = User.query.filter_by(id=student_id).first()

    if not student: raise exceptions.UserDosentExistError()
    if not lesson: raise exceptions.LessonDosentExistError()


    if student in lesson.students: raise exceptions.UserAlreadyAddedError()

    lesson.students.append(student)
    db.session.commit()

def remove_student_from_lesson(student_id, lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    student = User.query.filter_by(id=student_id).first()

    if not student: raise exceptions.UserDosentExistError()
    if not lesson: raise exceptions.LessonDosentExistError()


    if student in lesson.students:
        lesson.students.remove(student)
    else:
        raise exceptions.StudentNotInLesson()
    db.session.commit()

def get_all_lessons():
    results = Lesson.query.all()

    return results

def get_lesson(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    if not lesson: raise exceptions.LessonDosentExistError()

    return lesson

def remove_lesson(lesson_id):
    query = Lesson.query.filter_by(id=lesson_id)
    lesson = query.first()

    if not lesson: raise exceptions.LessonDosentExistError()

    lesson.students = []
    query.delete()
    db.session.commit()

    logging.info(f"Lesson with id {lesson_id} has been removed sucessfuly.")

def update_lesson_details(lesson_id, updates):
    lesson = Lesson.query.filter_by(id=lesson_id).first()

    if not lesson: raise exceptions.LessonDosentExistError()

    pre_lesson, info, homework = updates.get("pre_lesson"), updates.get("info"), updates.get("homework")

    if pre_lesson: lesson.pre_lesson = pre_lesson
    if info: lesson.info = info
    if homework: lesson.homework = homework
    db.session.commit()

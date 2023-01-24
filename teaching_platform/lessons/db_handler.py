import logging

import yaml
import jsonpickle

from teaching_platform.lessons import exceptions
from teaching_platform.models import User, Role, Lesson
from teaching_platform.extensions import db

with open("../config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

logging.basicConfig(level=logging.INFO, filemode="w", filename="../logs.log")
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

def add_lesson(teacher_id, info):
    teacher = User.query.filter_by(id=teacher_id, role=Role.TEACHER).first()
    if not teacher: raise exceptions.TeacherDosentExistError()
    lesson = Lesson(info=info, teacher=teacher)

    db.session.add(lesson)
    db.session.commit()

def add_student_to_lesson(student_id, lesson_id, teacher_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    student, teacher = User.query.filter_by(id=student_id).first(), User.query.filter_by(id=teacher_id).first()

    if not student: raise exceptions.UserDosentExistError()
    if not lesson: raise exceptions.LessonDosentExistError()

    if teacher.role != Role.ADMIN and lesson not in teacher.teaching: raise exceptions.AuthError()

    if student in lesson.students: raise exceptions.UserAlreadyAddedError()

    lesson.students.append(student)
    db.session.commit()

def get_all_lessons():
    results, lessons = Lesson.query.all(), []

    for lesson in results: lessons.append(lesson.get_json())
    return lessons

def get_lesson(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    if not lesson: raise exceptions.LessonDosentExistError()

    return lesson.get_json()

def remove_lesson(lesson_id, teacher_id):
    query, teacher = Lesson.query.filter_by(id=lesson_id), User.query.filter_by(id=teacher_id).first()
    lesson = query.first()

    if not lesson: raise exceptions.LessonDosentExistError()
    if teacher.role != Role.ADMIN and lesson not in teacher.teaching: raise exceptions.AuthError()

    query.delete()
    db.session.commit()

    logging.info(f"Lesson with id {lesson_id} has been removed sucessfuly.")

def update_lesson_details(lesson_id, teacher_id, updates):
    lesson, teacher = Lesson.query.filter_by(id=lesson_id).first(), User.query.filter_by(id=teacher_id).first()

    if not lesson: raise exceptions.LessonDosentExistError()
    if teacher.role != Role.ADMIN and lesson not in teacher.teaching: raise exceptions.AuthError()

    pre_lesson, info, homework = updates.get("pre_lesson"), updates.get("info"), updates.get("homework")

    if pre_lesson: lesson.pre_lesson = pre_lesson
    if info: lesson.info = info
    if homework: lesson.homework = homework
    db.session.commit()

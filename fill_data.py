from datetime import date, timedelta
import faker
from math import floor
from random import randint, choice, sample
import string
import sqlite3

from create_db import DATABASE


NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_LECTURERS = 5
NUMBER_COURSES = 8
APPROX_NUMBER_GRADES = 1000


def generate_fake_data() -> tuple():
    fake_students = []
    fake_groups = []
    fake_lecturers = []
    courses = set(["Фізика", "Математика", "Українська мова", "Англійська мова", "Історія України", "Всесвітня історія", "Українська література", "Хімія"])

    fake_data = faker.Faker("uk_UA")

    for _ in range(NUMBER_STUDENTS):
        fake_students.append(fake_data.name())

    for _ in range(NUMBER_GROUPS):
        fake_groups.append(f"{''.join([choice(string.ascii_uppercase) for i in range(3)])}-{''.join(choice(string.digits) for i in range(3))}")

    for _ in range(NUMBER_LECTURERS):
        fake_lecturers.append(fake_data.name())

    return fake_students, fake_groups, fake_lecturers, courses


def prepare_data(fake_students, fake_groups, fake_lecturers, courses) -> tuple():
    for_students = []
    for student in fake_students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))

    for_groups = []
    for group in fake_groups:
        for_groups.append((group, ))

    for_lecturers = []
    for lecturer in fake_lecturers:
        for_lecturers.append((lecturer, ))

    for_courses = []
    while courses:
        for_courses.append((courses.pop(), randint(1, NUMBER_LECTURERS)))

    for_grades = []
    n = 0
    date_of = date(2023, 9, 1)
    while n < APPROX_NUMBER_GRADES:
        date_of += timedelta(days=randint(0, 3))
        course_id = randint(1, NUMBER_COURSES)
        number_of_students = randint(floor(0.8*NUMBER_STUDENTS), NUMBER_STUDENTS)
        student_ids = sample(range(1, NUMBER_STUDENTS+1), k=number_of_students)
        for student_id in student_ids:
            for_grades.append((date_of, randint(0, 100), student_id, course_id))
        n += number_of_students

    return for_students, for_groups, for_lecturers, for_courses, for_grades


def insert_data_to_db(for_students, for_groups, for_lecturers, for_courses, for_grades) -> None:
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсору для маніпуляцій з даними

    with sqlite3.connect(DATABASE) as con:

        cur = con.cursor()

        sql_to_students = """INSERT INTO students (name, group_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_students, for_students)

        sql_to_groups = """INSERT INTO groups (title)
                               VALUES (?)"""
        cur.executemany(sql_to_groups, for_groups)

        sql_to_lecturers = """INSERT INTO lecturers (name)
                              VALUES (?)"""
        cur.executemany(sql_to_lecturers, for_lecturers)

        sql_to_courses = """INSERT INTO courses (title, lecturer_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_courses, for_courses)

        sql_to_grades = """INSERT INTO grades (date_of, grade, student_id, course_id)
                               VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_grades, for_grades)

        con.commit()


if __name__ == "__main__":
    for_students, for_groups, for_lecturers, for_courses, for_grades = prepare_data(*generate_fake_data())
    insert_data_to_db(for_students, for_groups, for_lecturers, for_courses, for_grades)
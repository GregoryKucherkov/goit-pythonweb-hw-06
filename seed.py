from connect import session
from models import Student, Group, Teacher, Subject, Grade
from faker import Faker
import random

fake = Faker()


def create_groups(number: int):
    groups = []
    for _ in range(number):
        group = Group(name=fake.word().capitalize())
        session.add(group)
        groups.append(group)
    session.commit()
    return groups


def create_students(number: int, groups):
    students = []
    for _ in range(number):
        group = random.choice(groups)
        student = Student(name=fake.name(), group_id=group.id)
        session.add(student)
        students.append(student)
    session.commit()
    return students


def create_teachers(number: int):
    teachers = []
    for _ in range(number):
        teacher = Teacher(name=fake.name())
        session.add(teacher)
        teachers.append(teacher)
    session.commit()
    return teachers


def create_subject(number: int, teachers):
    subjects = []

    for _ in range(number):
        teacher = random.choice(teachers)
        subject = Subject(name=fake.word().capitalize(), teacher_id=teacher.id)
        session.add(subject)
        subjects.append(subject)
    session.commit()
    return subjects


def create_grade(students, subjects):
    for student in students:
        for _ in range(random.randint(10, 21)):
            grade = Grade(
                grade=random.randint(1, 12),
                student=student,
                subject=random.choice(subjects),
            )
            session.add(grade)
    session.commit()


def clear_data():
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()
    session.commit()


def main():
    # in case we need to clear data before creating some new
    # clear_data()

    groups = create_groups(3)
    students = create_students(30, groups)
    teachers = create_teachers(5)
    subjects = create_subject(8, teachers)
    create_grade(students, subjects)
    session.close()


if __name__ == "__main__":
    main()

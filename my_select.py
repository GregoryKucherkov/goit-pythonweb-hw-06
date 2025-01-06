from connect import session
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy.sql import func
import random


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = (
        session.query(Student.name, func.avg(Grade.grade))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    print("1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів:")
    for student in result:
        print(f"{student.name}: {student[1]:.2f}")


# Знайти студента із найвищим середнім балом з певного предмета.
def select_2():
    result = (
        session.query(Student.name, Subject.name, func.avg(Grade.grade))
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .group_by(Student.id, Subject.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .all()
    )
    print("2. Знайти студента із найвищим середнім балом з певного предмета:")
    for student in result:
        print(f"{student[0]} in {student[1]}: {student[2]:.2f}")


# Знайти середній бал у групах з певного предмета.
def select_3():
    result = (
        session.query(Group.name, func.avg(Grade.grade))
        # .join(Group, Group.id == Student.group_id)
        .join(Student, Student.group_id == Group.id)  # Join Group to Student
        .join(Grade, Grade.student_id == Student.id)  # Join Student to Grade
        .join(Subject, Grade.subject_id == Subject.id)
        .group_by(Group.name)
        .all()
    )
    print("3. Знайти середній бал у групах з певного предмета:")
    for group in result:
        print(f"{group[0]} with average grade: {group[1]:.2f}")


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.avg(Grade.grade)).all()
    print("4. Знайти середній бал на потоці (по всій таблиці оцінок):")
    print(f"The avarage from all course: {result[0][0]:.2f}")


# Знайти які курси читає певний викладач. Версія де виводить усіх вчителів і предмети яку вони ведуть
def select_5():
    result = (
        session.query(Teacher.name, func.array_agg(Subject.name))
        .join(Subject, Subject.teacher_id == Teacher.id)
        .group_by(Teacher.id)
        .all()
    )
    print(
        "5.Знайти які курси читає певний викладач. Версія усіх вчителів і предмети яку вони ведуть:"
    )
    for teacher, subjects in result:
        print(f"{teacher} teaches {', '.join(subjects)}")


def select_teacher():
    group = session.query(Teacher.name).all()
    random_tuple = random.choice(group)
    return random_tuple[0]


# Версія де виводить усі предмети саме якогось вчителя
def select_5_1(teacher_name):
    result = (
        session.query(Teacher.name, func.array_agg(Subject.name))
        .join(Subject, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name == teacher_name)
        .group_by(Teacher.id)
        .all()
    )
    print("5_1. Версія де виводить усі предмети саме якогось вчителя: ")
    for teacher, subjects in result:
        if subjects:
            print(f"{teacher} teaches subject(s): {', '.join(subjects)}")
        else:
            print(f"{teacher} does not teach any subjects.")


def group_name():
    group = session.query(Group.name).all()
    random_tuple = random.choice(group)
    return random_tuple[0]


# Знайти список студентів у певній групі.
def select_6(group):
    result = (
        session.query(Student.name)
        .join(Group, Group.id == Student.group_id)
        .filter(Group.name == group)
        .all()
    )
    print(
        f"6. Знайти список студентів у певній групі: \nFor group: {group} - studens list is:"
    )
    for student in result:
        print(f"Student name: {student.name}")


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group):
    result = (
        session.query(Student.name, Grade.grade, Subject.name)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Group, Group.id == Student.group_id)
        .filter(Group.name == group)
        .all()
    )
    print(
        f"7. Знайти оцінки студентів у окремій групі з певного предмета.\nfor group {group}: "
    )
    for student_name, grade, subject_name in result:
        print(f"{student_name} has grade {grade} in {subject_name}")


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher):
    result = (
        session.query(Teacher.name, func.avg(Grade.grade))
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Teacher.name == teacher)
        .group_by(Teacher.id)
        .all()
    )
    print(
        f"8. Знайти середній бал, який ставить певний викладач зі своїх предметів.\nTeacher {teacher}: "
    )
    if not result:  # Check if result is empty
        print(f"Teacher {teacher} has not given any grades yet!")
    for teacher_name, avg_grade in result:
        print(f"{teacher_name} has an average grade of {avg_grade:.2f}")


def sudent_name():
    group = session.query(Student.name).all()
    random_tuple = random.choice(group)
    return random_tuple[0]


# Знайти список курсів, які відвідує певний студент.
def select_9(student):
    result = (
        session.query(Student.name, Subject.name)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Student.name == student)
        .all()
    )
    print("Знайти список курсів, які відвідує певний студент.")
    for student_name, subject_name in result:
        print(f"{student_name} is taking {subject_name}")


# Список курсів, які певному студенту читає певний викладач
def select_10(student):
    result = (
        session.query(Student.name, Subject.name, Teacher.name)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Student.name == student)
        # .filter(Teacher.name == teacher)     # if need filter by a specific teacher
        .all()
    )
    print("10. Список курсів, які певному студенту читає певний викладач:")
    for student_name, subject_name, teacher_name in result:
        print(f"{student_name} is taking {subject_name}, taught by {teacher_name}")


def main():
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    teacher = select_teacher()
    select_5_1(teacher)
    group_n = group_name()
    select_6(group_n)
    group_7 = group_name()
    select_7(group_7)
    teacher_8 = select_teacher()
    select_8(teacher_8)
    student = sudent_name()
    select_9(student)
    student_10 = sudent_name()
    select_10(student_10)
    session.close()


if __name__ == "__main__":
    main()

from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship("Group", back_populates="students")

    def __repr__(self) -> str:
        return f"Student(id={self.id}, name = {self.name})"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"Group(id={self.id}, name = {self.name})"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="teacher", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, name = {self.name})"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", onupdate="CASCADE")
    )
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")

    def __repr__(self) -> str:
        return f"Subject(id={self.id}, name = {self.name}, teacher = {self.teacher})"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    grade_date: Mapped[datetime] = mapped_column(default=func.now())
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
    )
    student: Mapped["Student"] = relationship("Student", back_populates="grades")

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", onupdate="CASCADE")
    )
    subject: Mapped["Subject"] = relationship("Subject")

    def __repr__(self) -> str:
        return f"Grade(id={self.id}, student={self.student}, subject= {self.subject}, grade = {self.grade}, grade_date = {self.grade_date})"

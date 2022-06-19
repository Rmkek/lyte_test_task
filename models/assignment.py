import enum
from models.student import Student
from models.teacher import Teacher
from sqlmodel import Field, Enum, SQLModel, Column, Relationship
from sqlalchemy import Integer, ForeignKey
from typing import Optional


class Assignment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    text: str
    confirmed_by_student: bool = Field(default=False)
    done: bool = Field(default=False)
    grade: Optional[int]  # [2:5]

    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")
    teacher: Optional[Teacher] = Relationship(back_populates="assignments")

    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    student: Optional[Student] = Relationship(back_populates="assignments")

from typing import List
from models.assignment import Assignment
from models.teacher import Teacher
from pydantic import BaseModel
from models.student import Student


class StudentTakeAssignmentResponse(BaseModel):
    student: Student
    assignments: List[Assignment]


class StudentDoneAssignmentResponse(BaseModel):
    student: Student
    assignment: Assignment


class TeacherAssignmentResponse(BaseModel):
    teacher: Teacher
    assignments: List[Assignment]

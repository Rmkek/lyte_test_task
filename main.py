from urllib import response
from api.api_requests import (
    AddTeacherAssignmentRequest,
    CreateStudentRequest,
    CreateTeacherRequest,
    StudentAssignmentRequest,
    TeacherAssignmentRequest,
)
from api.api_response import (
    StudentDoneAssignmentResponse,
    StudentTakeAssignmentResponse,
    TeacherAssignmentResponse,
)
from models.assignment import Assignment
from models.student import Student
from models.teacher import Teacher
from db import create_db_and_tables, clear_test_db, create_test_data

from typing import List
import time
from functools import wraps

from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException, Depends

# from endpoints.students import students


engine = create_db_and_tables("sqlite:///test_db.db")

clear_test_db(engine)
create_test_data(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.put("/api/student", tags=["student"], response_model=Student)
async def create_student(
    create_student_request: CreateStudentRequest,
    session: Session = Depends(get_session),
):
    student = Student(full_name=create_student_request.full_name)
    session.add(student)
    session.commit()

    return student


@app.get("/api/student", tags=["student"], response_model=Student)
async def get_student(full_name: str, session: Session = Depends(get_session)):
    student = session.exec(
        select(Student).where(
            Student.full_name == full_name,
        )
    ).first()

    return student


@app.post(
    "/api/student/take_assignment",
    tags=["student"],
    response_model=StudentTakeAssignmentResponse,
)
async def take_assignment(
    take_assignment: StudentAssignmentRequest, session: Session = Depends(get_session)
):
    assignment = session.exec(
        select(Assignment).where(
            Assignment.name == take_assignment.assignment_name,
        )
    ).first()
    student = session.exec(
        select(Student).where(
            Student.full_name == take_assignment.student_name,
        )
    ).first()
    student.assignments.append(assignment)
    session.add(student)
    session.commit()
    session.refresh(student)
    print(student.assignments)
    return StudentTakeAssignmentResponse(
        student=student, assignments=student.assignments
    )


@app.post(
    "/api/student/done_assignment",
    tags=["student"],
    response_model=StudentTakeAssignmentResponse,
)
async def take_assignment(
    take_assignment: StudentAssignmentRequest, session: Session = Depends(get_session)
):
    found_student = session.exec(
        select(Student, Assignment)
        .join(Assignment)
        .where(
            Assignment.name == take_assignment.assignment_name,
            Student.full_name == take_assignment.student_name,
        )
    ).first()

    found_student[1].confirmed_by_student = True
    session.add(found_student[1])
    session.commit()

    return StudentTakeAssignmentResponse(
        student=found_student[0], assignments=found_student[0].assignments
    )


@app.put("/api/teacher", tags=["teacher"], response_model=Teacher)
async def create_teacher(
    create_teacher_request: CreateTeacherRequest,
    session: Session = Depends(get_session),
):
    teacher = Teacher(full_name=create_teacher_request.full_name)
    session.add(teacher)
    session.commit()

    return teacher


@app.get("/api/teacher", tags=["teacher"], response_model=Teacher)
async def get_teacher(full_name: str, session: Session = Depends(get_session)):
    teacher = session.exec(
        select(Teacher).where(
            Teacher.full_name == full_name,
        )
    ).first()

    return teacher


@app.post("/api/teacher/add_assignment", tags=["teacher"], response_model=Assignment)
async def add_assignment(
    add_assignment_request: AddTeacherAssignmentRequest,
    session: Session = Depends(get_session),
):
    teacher = session.exec(
        select(Teacher).where(
            Teacher.full_name == add_assignment_request.teacher_name,
        )
    ).first()

    assignment = Assignment(
        teacher_id=teacher.id,
        teacher=teacher,
        name=add_assignment_request.name,
        text=add_assignment_request.text,
    )

    session.add(assignment)
    session.commit()

    if teacher.assignments:
        teacher.assignments.append(assignment)
    else:
        teacher.assignments = [assignment]

    session.add(teacher)
    session.commit()

    print("teach assignments: ", teacher.assignments)
    return assignment


@app.post(
    "/api/teacher/approve_assignment",
    tags=["teacher"],
    response_model=StudentTakeAssignmentResponse,
)
async def add_assignment(
    student_assignment: StudentAssignmentRequest,
    session: Session = Depends(get_session),
):
    found_student = session.exec(
        select(Student, Assignment)
        .join(Assignment)
        .where(
            Assignment.name == student_assignment.assignment_name,
            Student.full_name == student_assignment.student_name,
        )
    ).first()

    found_student[1].done = True
    session.add(found_student[1])
    session.commit()
    session.refresh(found_student[0])
    session.refresh(found_student[1])

    return StudentTakeAssignmentResponse(
        student=found_student[0], assignments=found_student[0].assignments
    )

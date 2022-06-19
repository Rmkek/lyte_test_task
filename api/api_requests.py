from pydantic import BaseModel


class CreateStudentRequest(BaseModel):
    full_name: str


class CreateTeacherRequest(BaseModel):
    full_name: str


class StudentAssignmentRequest(BaseModel):
    student_name: str
    assignment_name: str


class TeacherAssignmentRequest(BaseModel):
    teacher_name: str
    assignment_name: str


class AddTeacherAssignmentRequest(BaseModel):
    teacher_name: str
    name: str
    text: str

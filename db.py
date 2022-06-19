from sqlalchemy.engine.base import Engine
from models.assignment import Assignment
from models.student import Student
from models.teacher import Teacher
from sqlmodel import SQLModel, create_engine, Session, select

engine = None


def create_db_and_tables(db_url) -> Engine:
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

    SQLModel.metadata.create_all(engine)
    return engine


def clear_test_db(engine) -> None:
    with Session(engine) as session:
        assignments = session.exec(select(Assignment)).fetchall()
        students = session.exec(select(Student)).fetchall()
        teachers = session.exec(select(Teacher)).fetchall()

        deleted_data = assignments + students + teachers

        for each in deleted_data:
            session.delete(each)

        session.commit()


def create_test_data(engine) -> None:
    student_1 = Student(full_name="Student Studentovich Studentov")
    teacher_1 = Teacher(full_name="Teachering Teacher Teacherovich")
    assignment_1 = Assignment(
        name="Test assignment", text="Test description", teacher=teacher_1
    )
    assignment_2 = Assignment(
        name="Second assignment", text="Test description", teacher=teacher_1
    )
    teacher_1.assignments = [assignment_1, assignment_2]
    student_1.assignments = [assignment_1]

    with Session(engine) as session:
        session.add(student_1)
        session.add(teacher_1)
        session.add(assignment_1)
        session.add(assignment_2)
        session.commit()
        session.refresh(teacher_1)

        # print(teacher_1.assignments)


if __name__ == "__main__":
    create_db_and_tables("sqlite:///test_db.db")

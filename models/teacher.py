from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class Teacher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    full_name: str

    assignments: List["Assignment"] = Relationship(back_populates="teacher")
    students: Optional[int] = Field(default=None, foreign_key="student.id")

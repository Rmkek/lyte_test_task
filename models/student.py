from typing import List
from sqlmodel import Field, SQLModel, Relationship


class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    full_name: str
    assignments: List["Assignment"] = Relationship(back_populates="student")

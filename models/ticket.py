from sqlmodel import Field, SQLModel
from models import tier
from sqlalchemy import Enum, Column
import enum


class Status(enum.Enum):
    free = "FREE"
    sold = "SOLD"


class Ticket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tier_id: int = Field(foreign_key="tier.id")
    status: str = Field(Enum(Status))

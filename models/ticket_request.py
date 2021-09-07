from models import tier, ticket, reservation

from typing import Optional
from sqlmodel import Field, SQLModel


class TicketRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tier_id: int = Field(foreign_key="tier.id")
    ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
    reservation_id: int = Field(foreign_key="reservation.id")

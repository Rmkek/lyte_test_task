from db import create_db_and_tables
from models import reservation, ticket_request, ticket, tier

from fastapi import FastAPI
from sqlmodel import Session

app = FastAPI()
engine = None


@app.on_event("startup")
def on_startup():
    engine = create_db_and_tables()


@app.post("/api/v1/ticket-requests")
def create_hero(reservation_id: int, ticket_requests: list(ticket_request.TicketRequest)):
    # POST, accepts a list of RESERVATION_IDS and Ticket
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

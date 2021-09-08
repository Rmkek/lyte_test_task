from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel, create_engine, Session, select
from models.reservation import Reservation
from models.ticket import Ticket
from models.ticket_request import TicketRequest
from models.tier import Tier



def create_db_and_tables(db_url) -> Engine:
    # sqlite_file_name = "test_db"
    # sqlite_url = f"sqlite:///{sqlite_file_name}"

    # engine = create_engine(db_url, echo=True)
    engine = create_engine(db_url)
    
    SQLModel.metadata.create_all(engine)
    return engine


def clear_test_db(engine) -> None:
    with Session(engine) as session:
        tiers = session.exec(select(Tier)).fetchall()
        reservations = session.exec(select(Reservation)).fetchall()
        ticket_requests = session.exec(select(TicketRequest)).fetchall()
        tickets = session.exec(select(Ticket)).fetchall()

        deleted_data = tiers + reservations + ticket_requests + tickets

        for each in deleted_data:
            session.delete(each)

        session.commit()

def create_test_data(engine) -> None:
    tier_1 = Tier(name="Basic", price= 10.0, transfer_fee_percent=1.2)
    tier_2 = Tier(name="Extended", price= 20.0, transfer_fee_percent=1.4)

    reservation_1 = Reservation(email="test@test.com")
    reservation_2 = Reservation(email="test@protonmail.com")
    
    tiers_and_reservations = [tier_1, tier_2, reservation_1, reservation_2]

    with Session(engine) as session:
        # for some reason code below doesn't work
        # map(lambda each: session.add(each), commit_data)

        for each in tiers_and_reservations:
            session.add(each)
        session.commit()

        ticket_1 = Ticket(tier_id=tier_1.id, status="FREE")
        ticket_2 = Ticket(tier_id=tier_2.id, status="FREE")
        ticket_3 = Ticket(tier_id=tier_2.id, status="FREE")
        tickets = [ticket_1, ticket_2, ticket_3]

        for each in tickets:
            session.add(each)

        session.commit()


if __name__ == "__main__":
    create_db_and_tables("sqlite:///test_db.db")

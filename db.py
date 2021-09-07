from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel, create_engine, Session
from models.reservation import Reservation
from models.ticket import Ticket
from models.ticket_request import TicketRequest
from models.tier import Tier



def create_db_and_tables(db_url) -> Engine:
    # sqlite_file_name = "test_db"
    # sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(db_url, echo=True)
    
    SQLModel.metadata.create_all(engine)
    return engine


def create_test_data(engine) -> None:
    tier_1 = Tier(name="Basic", price= 10.0, transfer_fee_percent=1.2)
    tier_2 = Tier(name="Extended", price= 20.0, transfer_fee_percent=1.4)

    reservation_1 = Reservation(email="test@test.com")
    reservation_2 = Reservation(email="test@protonmail.com")
    
    ticket_1 = Ticket(tier_id=tier_1, status="FREE")
    ticket_2 = Ticket(tier_id=tier_2, status="FREE")
    ticket_3 = Ticket(tier_id=tier_2, status="FREE")

    commit_data = [tier_1, tier_2, reservation_1, reservation_2, ticket_1, ticket_2, ticket_3]

    with Session(engine) as session:
        map(lambda each: session.add(each), commit_data)
        session.commit()    


if __name__ == "__main__":
    create_db_and_tables("sqlite:///test_db.db")


from typing import Optional, List
from API.api_requests import APITicketRequest, APITicketWithReservationsRequest

from sqlmodel import Session, select
from db import create_db_and_tables, create_test_data
from models.reservation import Reservation
from fastapi import FastAPI


engine = create_db_and_tables('sqlite://')

create_test_data(engine)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post('/api/v1/ticket-requests')
async def read_item(ticket_requests: List[APITicketWithReservationsRequest]):
    print(ticket_requests)
    
    for request in ticket_requests:
        print('asdfasdf')
        with Session(engine) as session:
            reservations = session.exec(select(Reservation).where(Reservation.id == request.reservation_id))
            

    return {}
    # return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

from API.api_requests import APITicketRequest, APITicketWithReservationsRequest
from API.api_response import APITicketWithReservationsResponse, APIPerfomanceResponse
from API.exceptions import TicketRequestFailed

from models.reservation import Reservation
from models.ticket import Ticket
from models.tier import Tier

from db import create_db_and_tables, create_test_data, clear_test_db

from typing import Optional, List
from time import perf_counter
from functools import wraps
from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException


engine = create_db_and_tables('sqlite:///test_db.db')

clear_test_db(engine)
create_test_data(engine)

app = FastAPI()
requests_count = 0
average_process_time = 0

# TODO: fixme, there is smth wrong with request counting

def timed_and_counted(func):
    global requests_count, average_process_time
    requests_count += 1
    start_processing = perf_counter()
    try:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
    finally:
        end_time = perf_counter() - start_processing
        average_process_time = (average_process_time + end_time) / requests_count
    
    return wrapper

@app.post('/api/v1/ticket-requests', response_model=List[APITicketWithReservationsResponse])
@timed_and_counted
async def read_item(api_ticket_requests: List[APITicketWithReservationsRequest]):
    api_response: List[APITicketWithReservationsResponse] = []
    for user_request in api_ticket_requests:
        request_response: APITicketWithReservationsResponse = APITicketWithReservationsResponse(
            reservation_id=-1,
            reservation_cost=-1,
            reservation_fee=-1.0,
            ticket_requests=[]
        )

        with Session(engine) as session:
            reservations = session.exec(select(Reservation)
                                  .where(Reservation.id == user_request.reservation_id)).first()
            
            inner_transaction_succesful = True
            ticket_transaction = []
            reservation_cost = 0
            reservation_fee = 0
            
            try:
                for ticket_request in user_request.ticket_requests:
                    requested_tier_id = ticket_request.tier_id
                    tickets_with_tiers = session.exec(select(Ticket, Tier).join(Tier)
                                    .where(Ticket.tier_id == requested_tier_id, Ticket.status == "FREE")).first()
                    
                    if tickets_with_tiers is None:
                        raise TicketRequestFailed()

                    requested_ticket, requested_tier = tickets_with_tiers
        
                    requested_ticket.status = 'SOLD'
                    ticket_transaction.append(requested_ticket)
                    reservation_cost += requested_tier.price
                    reservation_fee += requested_tier.price * requested_tier.transfer_fee_percent

                    request_response.ticket_requests.append(APITicketRequest(ticket_request_id=ticket_request.ticket_request_id,
                                                                        tier_id=requested_tier_id,
                                                                        ticket_id=requested_ticket.id))
            except TicketRequestFailed as ticket_request_failed:
                raise HTTPException(status_code=400, detail=str(ticket_request_failed))
            
            for ticket in ticket_transaction:
                session.add(ticket)
            session.commit()

            request_response.reservation_id = user_request.reservation_id
            request_response.reservation_cost = reservation_cost
            request_response.reservation_fee = reservation_fee
            
            api_response.append(request_response)
            
    return api_response

@app.get('/api/v1/performance', response_model=APIPerfomanceResponse)
async def get_performance():
    global requests_count, average_process_time
    return APIPerfomanceResponse(requests_count=requests_count, average_process_time=average_process_time)

# TODO: add BLACK
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

from api.api_requests import APITicketRequest, APITicketWithReservationsRequest
from api.api_response import APITicketWithReservationsResponse, APIPerfomanceResponse
from api.exceptions import TicketRequestFailed
from models.ticket import Ticket
from models.tier import Tier
from db import create_db_and_tables, create_test_data, clear_test_db

from typing import List
import time
from functools import wraps

from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException


engine = create_db_and_tables("sqlite:///test_db.db")

clear_test_db(engine)
create_test_data(engine)

app = FastAPI()
requests_count = 0
average_process_time = 0


def measure_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global requests_count, average_process_time
        requests_count += 1

        start_time = time.time()

        try:
            response = await func(*args, **kwargs)
        except BaseException as ex:
            raise ex
        finally:
            average_process_time = (time.time() - start_time) / requests_count

        return response

    return wrapper


@app.post(
    "/api/v1/ticket-requests", response_model=List[APITicketWithReservationsResponse]
)
@measure_performance
async def get_tickets(api_ticket_requests: List[APITicketWithReservationsRequest]):
    api_response: List[APITicketWithReservationsResponse] = []
    try:
        for user_request in api_ticket_requests:
            request_response: APITicketWithReservationsResponse = (
                APITicketWithReservationsResponse(
                    reservation_id=-1,
                    reservation_cost=-1,
                    reservation_fee=-1.0,
                    ticket_requests=[],
                )
            )

            with Session(engine) as session:
                ticket_transaction = []
                reservation_cost = 0
                reservation_fee = 0

                for ticket_request in user_request.ticket_requests:
                    requested_tier_id = ticket_request.tier_id
                    tickets_with_tiers = session.exec(
                        select(Ticket, Tier)
                        .join(Tier)
                        .where(
                            Ticket.tier_id == requested_tier_id, Ticket.status == "FREE"
                        )
                    ).first()

                    if tickets_with_tiers is None:
                        raise TicketRequestFailed()

                    requested_ticket, requested_tier = tickets_with_tiers

                    requested_ticket.status = "SOLD"
                    ticket_transaction.append(requested_ticket)
                    reservation_cost += requested_tier.price
                    reservation_fee += (
                        requested_tier.price * requested_tier.transfer_fee_percent
                    )

                    request_response.ticket_requests.append(
                        APITicketRequest(
                            ticket_request_id=ticket_request.ticket_request_id,
                            tier_id=requested_tier_id,
                            ticket_id=requested_ticket.id,
                        )
                    )

                for ticket in ticket_transaction:
                    session.add(ticket)
                session.commit()

                request_response.reservation_id = user_request.reservation_id
                request_response.reservation_cost = reservation_cost
                request_response.reservation_fee = reservation_fee

                api_response.append(request_response)
    except TicketRequestFailed as ticket_request_failed:
        raise HTTPException(status_code=400, detail=str(ticket_request_failed))

    return api_response


@app.get("/api/v1/performance", response_model=APIPerfomanceResponse)
async def get_performance():
    global requests_count, average_process_time
    return APIPerfomanceResponse(
        requests_count=requests_count, average_process_time=average_process_time
    )

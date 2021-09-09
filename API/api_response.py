from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel
from .api_requests import APITicketRequest


class APITicketWithReservationsResponse(BaseModel):
    reservation_id: int
    reservation_cost: int
    reservation_fee: Decimal
    ticket_requests: List[APITicketRequest]


class APIPerfomanceResponse(BaseModel):
    average_process_time: Decimal
    requests_count: int

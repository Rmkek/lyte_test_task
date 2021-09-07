from typing import Optional, List
from pydantic import BaseModel


class APITicketRequest(BaseModel):
    ticket_request_id: int
    tier_id: int
    ticket_id: Optional[int]

class APITicketWithReservationsRequest(BaseModel):
    reservation_id: int
    ticket_requests: List[APITicketRequest]

from fastapi.testclient import TestClient

from main import app
from api.exceptions import TicketRequestFailed

client = TestClient(app)


def test_get_ticket_request_should_not_work():
    response = client.get("/api/v1/ticket-requests")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_post_ticket_request_with_empty_body():
    response = client.post("/api/v1/ticket-requests")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"loc": ["body"], "msg": "field required", "type": "value_error.missing"}
        ]
    }


def test_post_ticket_request_with_correct_body():
    request_body = [
        {
            "reservation_id": 1,
            "ticket_requests": [
                {"ticket_request_id": 1, "tier_id": 1, "ticket_id": None},
                {"ticket_request_id": 2, "tier_id": 2, "ticket_id": None},
            ],
        },
        {
            "reservation_id": 2,
            "ticket_requests": [
                {"ticket_request_id": 3, "tier_id": 2, "ticket_id": None}
            ],
        },
    ]

    response = client.post("/api/v1/ticket-requests", json=request_body)
    assert response.status_code == 200
    assert response.json() == [
        {
            "reservation_id": 1,
            "reservation_cost": 30,
            "reservation_fee": 40.0,
            "ticket_requests": [
                {"ticket_request_id": 1, "tier_id": 1, "ticket_id": 1},
                {"ticket_request_id": 2, "tier_id": 2, "ticket_id": 2},
            ],
        },
        {
            "reservation_id": 2,
            "reservation_cost": 20,
            "reservation_fee": 28.0,
            "ticket_requests": [{"ticket_request_id": 3, "tier_id": 2, "ticket_id": 3}],
        },
    ]


def test_post_ticker_request_second_time():
    request_body = [
        {
            "reservation_id": 1,
            "ticket_requests": [
                {"ticket_request_id": 1, "tier_id": 1, "ticket_id": None},
            ],
        },
    ]

    response = client.post("/api/v1/ticket-requests", json=request_body)
    assert response.status_code == 400
    assert response.json() == {"detail": str(TicketRequestFailed())}


def test_system_perfomance_after_two_requests():
    response = client.get("/api/v1/performance")
    assert response.status_code == 200
    assert response.json()["requests_count"] == 2


def test_system_perfomance_under_hundredth_of_a_second():
    response = client.get("/api/v1/performance")
    assert response.status_code == 200
    assert response.json()["average_process_time"] <= 0.01
    assert response.json()["requests_count"] == 2

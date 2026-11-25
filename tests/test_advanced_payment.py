import pytest
from app.server import app


def test_order_creation_failure(monkeypatch):

    from app import server

    def mock_create_order():
        raise Exception("Razorpay API unavailable")

    monkeypatch.setattr(
        server,
        "create_payment_order",
        mock_create_order
    )

    client = app.test_client()

    response = client.post("/create-order", headers={"Idempotency-Key": "advanced-failure-001"})

    assert response.status_code == 500
    assert response.json["success"] is False


@pytest.mark.parametrize(
    "payment_data",
    [
        {},
        {
            "razorpay_order_id": "order_test123",
            "razorpay_payment_id": "pay_test123"
        },
        {
            "razorpay_order_id": "order_test123",
            "razorpay_signature": "signature123"
        },
        {
            "razorpay_payment_id": "pay_test123",
            "razorpay_signature": "signature123"
        }
    ]
)
def test_missing_payment_fields(payment_data):

    client = app.test_client()

    response = client.post(
        "/verify-payment",
        json=payment_data
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_invalid_json_request():

    client = app.test_client()

    response = client.post(
        "/verify-payment",
        data="invalid-json",
        content_type="application/json"
    )

    assert response.status_code == 400


def test_payment_verification_service_error(monkeypatch):

    from app import server

    def mock_verification(data):
        raise Exception("Verification service unavailable")

    monkeypatch.setattr(
        server,
        "verify_payment_signature",
        mock_verification
    )

    client = app.test_client()

    payment_data = {
        "razorpay_order_id": "order_test123",
        "razorpay_payment_id": "pay_test123",
        "razorpay_signature": "signature123"
    }

    response = client.post(
        "/verify-payment",
        json=payment_data
    )

    assert response.status_code == 500
    assert response.json["success"] is False


def test_multiple_order_creation_requests(monkeypatch):

    from app import server

    order_counter = {"count": 0}

    def mock_create_order():

        order_counter["count"] += 1

        return {
            "id": f"order_test{order_counter['count']}",
            "amount": 49900,
            "currency": "INR"
        }

    monkeypatch.setattr(
        server,
        "create_payment_order",
        mock_create_order
    )

    client = app.test_client()

    first_response = client.post("/create-order", headers={"Idempotency-Key": "advanced-order-001"})
    second_response = client.post("/create-order", headers={"Idempotency-Key": "advanced-order-002"})

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert (
        first_response.json["order_id"]
        != second_response.json["order_id"]
    )

    assert order_counter["count"] == 2

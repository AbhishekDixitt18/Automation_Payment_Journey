from app.server import app


def test_health_api():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_create_payment_order(monkeypatch):

    from app import server

    def mock_create_order():

        return {
            "id": "order_test123",
            "amount": 49900,
            "currency": "INR"
        }

    monkeypatch.setattr(
        server,
        "create_payment_order",
        mock_create_order
    )

    client = app.test_client()

    response = client.post("/create-order", headers={"Idempotency-Key": "api-order-test-001"})

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["order_id"] == "order_test123"


def test_valid_payment_signature(monkeypatch):

    from app import server

    monkeypatch.setattr(
        server,
        "verify_payment_signature",
        lambda data: True
    )

    client = app.test_client()

    payment_data = {
        "razorpay_order_id": "order_test123",
        "razorpay_payment_id": "pay_test123",
        "razorpay_signature": "valid_test_signature"
    }

    response = client.post(
        "/verify-payment",
        json=payment_data
    )

    assert response.status_code == 200
    assert response.json["success"] is True


def test_invalid_payment_signature(monkeypatch):

    from app import server

    monkeypatch.setattr(
        server,
        "verify_payment_signature",
        lambda data: False
    )

    client = app.test_client()

    payment_data = {
        "razorpay_order_id": "order_test123",
        "razorpay_payment_id": "pay_test123",
        "razorpay_signature": "invalid_test_signature"
    }

    response = client.post(
        "/verify-payment",
        json=payment_data
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_missing_payment_details():

    client = app.test_client()

    response = client.post(
        "/verify-payment",
        json={}
    )

    assert response.status_code == 400


def test_invalid_request_body():

    client = app.test_client()

    response = client.post("/verify-payment")

    assert response.status_code == 400

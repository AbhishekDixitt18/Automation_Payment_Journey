from app.server import app


def test_duplicate_request_returns_same_order(monkeypatch):

    from app import server

    order_counter = {"count": 0}

    def mock_create_order():

        order_counter["count"] += 1

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

    headers = {
        "Idempotency-Key": "test-payment-001"
    }

    first_response = client.post(
        "/create-order",
        headers=headers
    )

    second_response = client.post(
        "/create-order",
        headers=headers
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert (
        first_response.json["order_id"]
        == second_response.json["order_id"]
    )

    assert order_counter["count"] == 1


def test_different_keys_create_different_orders(monkeypatch):

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

    first_response = client.post(
        "/create-order",
        headers={"Idempotency-Key": "payment-001"}
    )

    second_response = client.post(
        "/create-order",
        headers={"Idempotency-Key": "payment-002"}
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert (
        first_response.json["order_id"]
        != second_response.json["order_id"]
    )

    assert order_counter["count"] == 2


def test_missing_idempotency_key():

    client = app.test_client()

    response = client.post("/create-order")

    assert response.status_code == 400
    assert response.json["success"] is False


def test_invalid_long_idempotency_key():

    client = app.test_client()

    response = client.post(
        "/create-order",
        headers={"Idempotency-Key": "A" * 129}
    )

    assert response.status_code == 400

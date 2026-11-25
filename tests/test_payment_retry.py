from app.server import app


def test_retry_after_failed_payment_creates_new_order(monkeypatch):

    from app import server

    order_counter = {"count": 0}

    def mock_create_order():

        order_counter["count"] += 1

        return {
            "id": f"order_retry_{order_counter['count']}",
            "amount": 49900,
            "currency": "INR"
        }

    monkeypatch.setattr(
        server,
        "create_payment_order",
        mock_create_order
    )

    # Simulate payment signature verification failure
    monkeypatch.setattr(
        server,
        "verify_payment_signature",
        lambda data: False
    )

    client = app.test_client()

    # First payment attempt
    first_response = client.post(
        "/create-order",
        headers={"Idempotency-Key": "retry-attempt-001"}
    )

    assert first_response.status_code == 200

    first_order_id = first_response.json["order_id"]

    # Simulate failed payment verification
    payment_data = {
        "razorpay_order_id": first_order_id,
        "razorpay_payment_id": "pay_failed_test",
        "razorpay_signature": "invalid_signature"
    }

    verification_response = client.post(
        "/verify-payment",
        json=payment_data
    )

    assert verification_response.status_code == 400
    assert verification_response.json["success"] is False

    # Second payment attempt with a new idempotency key
    second_response = client.post(
        "/create-order",
        headers={"Idempotency-Key": "retry-attempt-002"}
    )

    assert second_response.status_code == 200

    second_order_id = second_response.json["order_id"]

    # Verify that retry created a new order
    assert first_order_id != second_order_id
    assert order_counter["count"] == 2

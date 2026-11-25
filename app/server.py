from flask import Flask, render_template, jsonify, request
from threading import Lock

from app.payment_service import (
    create_payment_order,
    verify_payment_signature
)

from config.settings import RAZORPAY_KEY_ID


app = Flask(__name__)

# In-memory idempotency storage for this demo
idempotency_store = {}
idempotency_lock = Lock()


@app.route("/")
def home():

    return render_template(
        "index.html",
        razorpay_key=RAZORPAY_KEY_ID
    )


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "application": "Payment Automation Framework"
    })


@app.route("/create-order", methods=["POST"])
def create_order():

    idempotency_key = request.headers.get("Idempotency-Key")

    if not idempotency_key:
        return jsonify({
            "success": False,
            "message": "Idempotency key is required"
        }), 400

    if len(idempotency_key) > 128:
        return jsonify({
            "success": False,
            "message": "Invalid idempotency key"
        }), 400

    try:

        with idempotency_lock:

            if idempotency_key in idempotency_store:

                return jsonify(
                    idempotency_store[idempotency_key]
                )

            order = create_payment_order()

            response_data = {
                "success": True,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "key": RAZORPAY_KEY_ID
            }

            idempotency_store[idempotency_key] = response_data

            return jsonify(response_data)

    except Exception:

        app.logger.exception("Order creation failed")

        return jsonify({
            "success": False,
            "message": "Unable to create payment order"
        }), 500


@app.route("/verify-payment", methods=["POST"])
def verify_payment():

    try:

        payment_data = request.get_json(silent=True)

        if not isinstance(payment_data, dict):
            return jsonify({
                "success": False,
                "message": "Invalid payment data"
            }), 400

        required_fields = [
            "razorpay_order_id",
            "razorpay_payment_id",
            "razorpay_signature"
        ]

        if not all(payment_data.get(field) for field in required_fields):
            return jsonify({
                "success": False,
                "message": "Missing payment verification details"
            }), 400

        verified = verify_payment_signature(payment_data)

        if verified:

            return jsonify({
                "success": True,
                "message": "Payment verified successfully"
            })

        return jsonify({
            "success": False,
            "message": "Payment signature verification failed"
        }), 400

    except Exception:

        app.logger.exception("Payment verification failed")

        return jsonify({
            "success": False,
            "message": "Unable to verify payment"
        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

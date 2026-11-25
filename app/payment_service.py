import razorpay
import uuid

from config.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET
)


def get_razorpay_client():

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise RuntimeError(
            "Razorpay test credentials are missing. "
            "Configure them in your .env file."
        )

    return razorpay.Client(
        auth=(
            RAZORPAY_KEY_ID,
            RAZORPAY_KEY_SECRET
        )
    )


def create_payment_order():

    client = get_razorpay_client()

    order_data = {
        "amount": 49900,
        "currency": "INR",
        "receipt": f"payment_test_{uuid.uuid4().hex[:12]}"
    }

    order = client.order.create(
        data=order_data
    )

    return order


def verify_payment_signature(payment_data):

    client = get_razorpay_client()

    try:
        client.utility.verify_payment_signature(
            payment_data
        )
        return True

    except razorpay.errors.SignatureVerificationError:
        return False
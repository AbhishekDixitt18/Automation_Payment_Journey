import os

from dotenv import load_dotenv

load_dotenv()

BROWSER = os.getenv("BROWSER", "chrome")

HEADLESS = (
    os.getenv("HEADLESS", "false").lower() == "true"
)

TIMEOUT = int(os.getenv("TIMEOUT", "15"))

BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:5000"
)

RAZORPAY_KEY_ID = os.getenv(
    "RAZORPAY_KEY_ID",
    ""
)

RAZORPAY_KEY_SECRET = os.getenv(
    "RAZORPAY_KEY_SECRET",
    ""
)
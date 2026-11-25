# Payment Automation Framework

A Python-based payment automation testing framework that integrates **Razorpay Test Mode**, **Selenium WebDriver**, and **Pytest** to automate and validate payment workflows.

The project demonstrates UI automation, API testing, payment verification, idempotency, retry handling, and end-to-end payment testing.

---

## Project Overview

The framework simulates an online checkout experience where users can initiate a payment, complete the Razorpay test payment process, and verify the payment response.

It is designed to test important payment scenarios and identify issues such as:

- Payment failures and verification errors.
- Duplicate payment-order creation.
- Repeated payment requests.
- Checkout UI failures.
- Payment retry and recovery scenarios.
- End-to-end payment workflow failures.

**Note:** This project uses Razorpay Test Mode. No real money is transferred.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Main programming language |
| Flask | Backend application |
| Razorpay SDK | Payment order creation and signature verification |
| Selenium WebDriver | Browser automation |
| Pytest | Test execution and test management |
| Requests | API testing |
| pytest-html | HTML test reports |
| HTML, CSS, JavaScript | Checkout interface |
| python-dotenv | Environment variable management |

---

## Project Structure

```text
Payment-Automation-Framework/
│
├── app/
│   ├── __init__.py
│   ├── server.py
│   ├── payment_service.py
│   └── templates/
│       └── index.html
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_payment.py
│   ├── test_payment_api.py
│   ├── test_advanced_payment.py
│   ├── test_idempotency.py
│   ├── test_payment_retry.py
│   ├── test_payment_e2e.py
│   └── pages/
│       ├── __init__.py
│       └── checkout_page.py
│
├── utils/
│   ├── __init__.py
│   └── driver_factory.py
│
├── conftest.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

### Directory Description

- **app/** – Contains the Flask application, payment services, and checkout page.
- **config/** – Handles application configuration and environment settings.
- **tests/** – Contains UI, API, advanced, retry, idempotency, and end-to-end tests.
- **tests/pages/** – Implements the Page Object Model for checkout interactions.
- **utils/** – Contains reusable browser-driver utilities.
- **conftest.py** – Provides shared Pytest fixtures.

---

## Key Features

### 1. Payment Order Creation
Creates Razorpay payment orders through the backend using the Razorpay SDK.

### 2. Payment Signature Verification
Validates payment signatures to verify whether the payment response is authentic.

### 3. UI Automation
Uses Selenium WebDriver to automate checkout page interactions and validate UI elements.

### 4. API Testing
Tests backend endpoints, including:

- `GET /health`
- `POST /create-order`
- `POST /verify-payment`

### 5. Idempotency Testing
Checks whether repeated requests with the same idempotency key return the existing order response instead of creating another order.

### 6. Retry Testing
Validates payment retry behaviour after unsuccessful or interrupted payment attempts.

### 7. End-to-End Testing
Automates the complete checkout journey using Razorpay Test Mode and verifies the final payment status.

### 8. HTML Test Reports
Generates detailed test execution reports using pytest-html.

---

## Prerequisites

Install the following before running the project:

- Python 3.13 or compatible Python version.
- Google Chrome.
- Git.
- Razorpay Test Mode account and API credentials.

Selenium Manager automatically handles browser-driver management in supported environments.

---

## Installation and Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/AbhishekDixitt18/Automation_Payment_Journey.git
```

### 2. Navigate to the Project

```powershell
cd Automation_Payment_Journey
```

### 3. Create a Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root.

You can copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Add your Razorpay Test Mode credentials to `.env`:

```env
BROWSER=chrome
HEADLESS=false
TIMEOUT=15

BASE_URL=http://127.0.0.1:5000

RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret
```

**Security:** Never commit your `.env` file or expose your Razorpay secret key. The `.gitignore` file excludes `.env` from Git tracking.

---

## Running the Application

Start the Flask application:

```powershell
python -m app.server
```

Open the checkout page:

```text
http://127.0.0.1:5000
```

The application provides a demo checkout experience with a payment amount of ₹499.

---

## Running Automated Tests

Make sure the Flask application is running before executing tests that interact with the application.

### Run All Tests

```powershell
pytest -v
```

### Run UI Tests

```powershell
pytest tests/test_payment.py -v
```

### Run API Tests

```powershell
pytest tests/test_payment_api.py -v
```

### Run Idempotency Tests

```powershell
pytest tests/test_idempotency.py -v
```

### Run Retry Tests

```powershell
pytest tests/test_payment_retry.py -v
```

### Run End-to-End Tests

```powershell
pytest tests/test_payment_e2e.py -v -s
```

---

## Generate HTML Test Reports

Execute the complete test suite and generate a self-contained HTML report:

```powershell
pytest -v --html=reports/full-report.html --self-contained-html
```

Open the report:

```powershell
Invoke-Item reports\full-report.html
```

The report provides an overview of test execution, including passed and failed test cases.

---

## Test Coverage

The framework includes test scenarios for:

| Testing Area | Validation |
|---|---|
| Checkout UI | Page loading and payment button behaviour |
| Payment API | Backend endpoint responses |
| Payment Order | Order creation and response validation |
| Signature Verification | Payment signature validation |
| Idempotency | Duplicate request handling |
| Retry Handling | Payment retry behaviour |
| End-to-End | Complete payment workflow |

The project has successfully executed **23 automated tests** in the local test environment.

---

## Important Implementation Notes

- Payments are performed using Razorpay Test Mode.
- The application uses environment variables for sensitive configuration.
- Idempotency is implemented using an in-memory store for demonstration purposes.
- The in-memory idempotency implementation is not intended for production use. A production system should use persistent storage such as Redis or a database with atomic uniqueness controls.
- End-to-end payment tests interact with the Razorpay test checkout interface and may require updates if that interface changes.

---

## Future Enhancements

- Integrate CI/CD using Jenkins or GitHub Actions.
- Add database-backed transaction management.
- Implement persistent idempotency using Redis.
- Expand negative and boundary test scenarios.
- Add cross-browser testing.
- Integrate structured logging and test execution notifications.

---

## Author

**Abhishek Dixit**

Computer Science Undergraduate | Automation Testing | Python | Selenium | API Testing | DevOps

**GitHub Repository:**  
https://github.com/AbhishekDixitt18/Automation_Payment_Journey
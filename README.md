\# Payment Automation Framework



An end-to-end payment automation testing framework built using Python, Selenium WebDriver, Pytest, Flask, and Razorpay Test Mode.



The framework automates and validates payment checkout workflows, API operations, payment verification, idempotency, and retry scenarios.



\## Features



\- Browser automation using Selenium WebDriver.

\- Test execution and organization using Pytest.

\- Razorpay Test Mode integration.

\- Payment order creation and signature verification.

\- UI and API testing.

\- Idempotency and duplicate-request testing.

\- Payment retry testing.

\- Page Object Model (POM).

\- HTML test reporting with pytest-html.

\- Environment-based configuration.



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python 3.13 | Programming language |

| Flask | Backend application |

| Selenium | Browser automation |

| Pytest | Testing framework |

| pytest-html | HTML reporting |

| Razorpay | Payment gateway |

| python-dotenv | Environment configuration |

| Chrome | Automation browser |



\## Project Structure



```text

Payment-Automation-Framework/

â”‚

â”œâ”€â”€ app/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â”œâ”€â”€ server.py

â”‚   â”œâ”€â”€ payment\_service.py

â”‚   â””â”€â”€ templates/

â”‚       â””â”€â”€ index.html

â”‚

â”œâ”€â”€ config/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â””â”€â”€ settings.py

â”‚

â”œâ”€â”€ tests/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â”œâ”€â”€ conftest.py

â”‚   â”œâ”€â”€ test\_payment.py

â”‚   â”œâ”€â”€ test\_payment\_api.py

â”‚   â”œâ”€â”€ test\_advanced\_payment.py

â”‚   â”œâ”€â”€ test\_idempotency.py

â”‚   â”œâ”€â”€ test\_payment\_retry.py

â”‚   â”œâ”€â”€ test\_payment\_e2e.py

â”‚   â””â”€â”€ pages/

â”‚       â”œâ”€â”€ \_\_init\_\_.py

â”‚       â””â”€â”€ checkout\_page.py

â”‚

â”œâ”€â”€ utils/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â””â”€â”€ driver\_factory.py

â”‚

â”œâ”€â”€ conftest.py

â”œâ”€â”€ config/

â”œâ”€â”€ .env.example

â”œâ”€â”€ .gitignore

â”œâ”€â”€ pytest.ini

â”œâ”€â”€ requirements.txt

â””â”€â”€ README.md

```



\## Prerequisites



\- Python 3.13 or later

\- Google Chrome

\- Git

\- Razorpay Test Mode API credentials



\## Installation



\### 1. Clone the repository



```powershell

git clone https://github.com/AbhishekDixitt18/Automation\_Payment\_Journey.git

cd Automation\_Payment\_Journey

```



\### 2. Create a virtual environment



```powershell

python -m venv venv

```



\### 3. Activate the environment



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 4. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 5. Configure environment variables



Create a `.env` file in the project root using `.env.example` as a reference.



Configure your own Razorpay Test Mode credentials:



```env

BROWSER=chrome

HEADLESS=false

TIMEOUT=15

BASE\_URL=http://127.0.0.1:5000



RAZORPAY\_KEY\_ID=rzp\_test\_your\_key\_id

RAZORPAY\_KEY\_SECRET=your\_test\_key\_secret

```



Never upload `.env` or expose API secrets publicly.



\## Running the Application



Start Flask:



```powershell

python -m app.server

```



Open:



`http://127.0.0.1:5000`



Health check:



`http://127.0.0.1:5000/health`



\## Running Tests



Keep Flask running in one PowerShell window. Use another terminal for test execution.



Run the complete test suite:



```powershell

pytest -v

```



Run UI tests:



```powershell

pytest tests/test\_payment.py -v

```



Run API tests:



```powershell

pytest tests/test\_payment\_api.py -v

```



Run end-to-end payment testing:



```powershell

pytest tests/test\_payment\_e2e.py -v -s

```



The E2E test uses Razorpay Test Mode and automated browser interactions.



\## HTML Test Reports



Generate a self-contained HTML report:



```powershell

pytest -v --html=reports/full-report.html --self-contained-html

```



Open the report:



```powershell

Invoke-Item reports/full-report.html

```



\## Test Results



The complete test suite successfully passed:



\*\*23 passed in 55.60 seconds.\*\*



Coverage includes:



\- Checkout UI validation.

\- Payment API validation.

\- Payment order creation.

\- Payment signature verification.

\- Advanced payment scenarios.

\- Idempotency testing.

\- Payment retry testing.

\- End-to-end Razorpay Test Mode

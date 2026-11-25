import pytest
import time
from selenium import webdriver


@pytest.fixture
def driver():

    options = webdriver.ChromeOptions()

    # Keep Chrome visible
    options.add_argument("--start-maximized")

    browser = webdriver.Chrome(options=options)

    # Wait after Chrome opens
    time.sleep(3)

    yield browser

    # Keep the browser visible after the test
    time.sleep(2)

    browser.quit()


@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000"

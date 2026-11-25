from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.settings import BROWSER, HEADLESS


def create_driver():

    if BROWSER.lower() == "chrome":

        options = Options()

        options.add_argument("--start-maximized")

        options.add_argument("--disable-notifications")

        if HEADLESS:
            options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)

    elif BROWSER.lower() == "edge":

        driver = webdriver.Edge()

    else:

        raise ValueError(
            f"Unsupported browser: {BROWSER}"
        )

    return driver
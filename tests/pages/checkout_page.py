from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:

    PAY_BUTTON = (By.ID, "pay-button")
    STATUS_MESSAGE = (By.ID, "status")

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, base_url):

        self.driver.get(base_url)

    def get_title(self):

        return self.driver.title

    def is_payment_button_visible(self):

        return self.wait.until(
            EC.visibility_of_element_located(
                self.PAY_BUTTON
            )
        ).is_displayed()

    def is_payment_button_enabled(self):

        button = self.wait.until(
            EC.presence_of_element_located(
                self.PAY_BUTTON
            )
        )

        return button.is_enabled()

    def get_status_message(self):

        return self.driver.find_element(
            *self.STATUS_MESSAGE
        ).text
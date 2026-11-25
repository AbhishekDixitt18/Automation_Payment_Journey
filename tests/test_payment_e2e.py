from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def skip_optional_prompt(driver):
    try:
        button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Maybe later']")
            )
        )
        button.click()
    except Exception:
        pass


def test_razorpay_payment_end_to_end(driver, base_url):

    wait = WebDriverWait(driver, 30)

    # 1. Open application
    driver.get(base_url)

    # 2. Open Razorpay checkout
    wait.until(
        EC.element_to_be_clickable((By.ID, "pay-button"))
    ).click()

    frame = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "razorpay-checkout-frame")
        )
    )

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(frame)
    )

    print("Razorpay checkout opened.")

    # 3. Enter mobile number
    wait.until(
        EC.element_to_be_clickable((By.NAME, "contact"))
    ).send_keys("9000090000")

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Continue']")
        )
    ).click()

    print("Mobile number submitted.")

    # 4. Select Add a new card
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[normalize-space()='Add a new card']")
        )
    ).click()

    # 5. Enter Razorpay test card details
    wait.until(
        EC.element_to_be_clickable((By.NAME, "card.number"))
    ).send_keys("5267318187975449")

    driver.find_element(
        By.NAME, "card.expiry"
    ).send_keys("12/30")

    driver.find_element(
        By.NAME, "card.cvv"
    ).send_keys("123")

    # 6. Submit card
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-test-id='add-card-cta']")
        )
    ).click()

    print("Test card submitted.")

    # 7. Skip optional save-card prompt
    skip_optional_prompt(driver)

    # 8. Continue to bank authentication
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Continue']")
        )
    ).click()

    # 9. Skip optional RBI prompt
    skip_optional_prompt(driver)

    # 10. Wait for OTP field
    wait.until(
        EC.presence_of_element_located((By.NAME, "otp"))
    )

    print("Bank OTP screen reached.")

    # 11. Enter test OTP using JavaScript
    driver.execute_script("""
        const otp = document.querySelector('input[name="otp"]');

        if (!otp) {
            throw new Error("OTP field not found.");
        }

        const setter = Object.getOwnPropertyDescriptor(
            HTMLInputElement.prototype, 'value'
        ).set;

        setter.call(otp, '1111');

        otp.dispatchEvent(new Event('input', { bubbles: true }));
        otp.dispatchEvent(new Event('change', { bubbles: true }));
    """)

    otp_value = driver.execute_script(
        "return document.querySelector('input[name=\"otp\"]').value;"
    )

    assert otp_value == "1111", "Test OTP was not entered."

    print("Test OTP entered successfully.")

    # 12. Submit bank OTP
    continue_buttons = [
        button
        for button in driver.find_elements(
            By.XPATH, "//button[normalize-space()='Continue']"
        )
        if button.is_displayed() and button.is_enabled()
    ]

    assert continue_buttons, "Bank Continue button not found."

    driver.execute_script(
        "arguments[0].click();",
        continue_buttons[-1]
    )

    print("Bank OTP submitted.")

    # 13. Return to main application
    driver.switch_to.default_content()

    # 14. Wait for the final payment result
    print("Waiting for payment verification...")

    result_wait = WebDriverWait(driver, 60)

    def payment_result_received(browser):
        try:
            message = browser.find_element(By.ID, "status").text
            if (
                "Payment Successful" in message
                or "Payment Failed" in message
                or "Verification Failed" in message
            ):
                return message
        except Exception:
            pass

        return False

    result = result_wait.until(payment_result_received)

    print("Payment result:", result)

    assert "Payment Successful" in result, (
        f"Payment was not successful. Result: {result}"
    )

    assert "Signature Verified" in result, (
        f"Payment signature verification failed. Result: {result}"
    )

    print("END-TO-END PAYMENT TEST PASSED.")

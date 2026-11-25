from tests.pages.checkout_page import CheckoutPage


def test_checkout_page_loads(driver, base_url):

    checkout = CheckoutPage(driver)

    checkout.open(base_url)

    assert checkout.get_title() == "Payment Automation Framework"


def test_payment_button_visible(driver, base_url):

    checkout = CheckoutPage(driver)

    checkout.open(base_url)

    assert checkout.is_payment_button_visible()


def test_payment_button_enabled(driver, base_url):

    checkout = CheckoutPage(driver)

    checkout.open(base_url)

    assert checkout.is_payment_button_enabled()
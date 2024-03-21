import logging

from framework.components import input_field, button

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


class LoginLocators():
    email_locator = '//input[@id="loginusername"]'
    password_locator = '//input[@id="loginpassword"]'
    log_in_button_locator = '//div[@class="modal-footer"]//button[text()="Log in" ]'
    close_button_locator = '//div[@class="modal-footer"]//button[text()="Close" ]'


class LoginPage(LoginLocators):
    def __init__(self):
        super().__init__()
        self.email = input_field.InputField(locator=self.email_locator)
        self.password = input_field.InputField(locator=self.password_locator)
        self.log_in = button.Button(locator=self.log_in_button_locator)
        self.close = button.Button(locator=self.close_button_locator)

    def perform_login(self, username="andra@gmail.com", pasword="1234"):
        LOG.info("Trying to perform login . . . ")
        self.email.wait_until_is_displayed()
        self.email.send_key(value=username)
        self.password.wait_until_is_displayed()
        self.password.send_key(value=pasword)
        self.log_in.wait_until_is_displayed()
        self.log_in.click()
        self.log_in.wait_until_is_not_displayed()

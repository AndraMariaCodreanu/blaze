from framework.components import input_field, button


class SignUpLocators:
    email_locator = '//input[@id="sign-username"]'
    password_locator = '//input[@id="sign-password"]'
    sign_up_button_locator = '//div[@class="modal-footer"]//button[text()="Sign up"]'
    close_button_locator = '//div[@class="modal-footer"]//button[text()="Close"]'


class SignUpPage(SignUpLocators):
    def __init__(self):
        super().__init__()
        self.email = input_field.InputField(locator=self.email_locator)
        self.password = input_field.InputField(locator=self.password_locator)
        self.sign_up = button.Button(locator=self.sign_up_button_locator)
        self.close = button.Button(locator=self.close_button_locator)

    def create_account(self, email, password):
        self.email.send_key(email)
        self.password.send_key(password)
        self.sign_up.click()
        self.sign_up.wait_until_is_not_displayed()

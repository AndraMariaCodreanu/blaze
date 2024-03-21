from framework.components import button, base_component


class HeaderLocators:
    home_button_locator = '//a[text()="Home "]'
    contact_button_locator = '//a[text()="Contact"]'
    about_us_button_locator = '//a[text()="About us"]'
    cart_button_locator = '//a[text()="Cart"]'
    log_in_button_locator = '//a[text()="Log in"]'
    sign_up_button_locator = '//a[text()="Sign up"]'
    log_out_button_locator = '//a[text()="Log out"]'


class Header(HeaderLocators, base_component.BaseComponent):
    def __init__(self, locator):
        super().__init__(locator=locator)
        self.home = button.Button(f'{self._locator}{self.home_button_locator}')
        self.contact = button.Button(f'{self._locator}{self.contact_button_locator}')
        self.about_us = button.Button(f'{self._locator}{self.about_us_button_locator}')
        self.cart = button.Button(f'{self._locator}{self.cart_button_locator}')
        self.log_in = button.Button(f'{self._locator}{self.log_in_button_locator}')
        self.sign_up = button.Button(f'{self._locator}{self.sign_up_button_locator}')
        self.log_out = button.Button(f'{self._locator}{self.log_out_button_locator}')

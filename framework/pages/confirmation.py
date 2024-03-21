from framework.components import base_component, button, text_field


class ConfirmationLocators:
    thank_you_title_locator = '//div[contains(@class,"sweet-alert")]//h2'
    purchase_details_locator = '//div[contains(@class,"sweet-alert")]//p'
    ok_button_locator = '//button[contains(@class,"confirm")]'


class ConfirmationPage(base_component.BaseComponent, ConfirmationLocators):
    def __init__(self):
        super().__init__()
        self.thank_you = text_field.TextField(locator=self.thank_you_title_locator)
        self.ok = button.Button(locator=self.ok_button_locator)
        self.purchase_details = text_field.TextField(locator=self.purchase_details_locator)

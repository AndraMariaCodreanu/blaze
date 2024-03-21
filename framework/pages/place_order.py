from framework.components import button, input_field


class PlaceOrderLocators:
    name_locator = '//input[@id="name"]'
    country_locator = '//input[@id="country"]'
    city_locator = '//input[@id="city"]'
    credit_card_locator = '//input[@id="card"]'
    month_locator = '//input[@id="month"]'
    year_locator = '//input[@id="year"]'
    purchase_button_locator = '//button[text()="Purchase"]'


class PlaceOrderPage(PlaceOrderLocators):
    def __init__(self):
        super().__init__()
        self.name = input_field.InputField(self.name_locator)
        self.country = input_field.InputField(self.country_locator)
        self.city = input_field.InputField(self.city_locator)
        self.credit_card = input_field.InputField(self.credit_card_locator)
        self.month = input_field.InputField(self.month_locator)
        self.year = input_field.InputField(self.year_locator)
        self.purchase = button.Button(self.purchase_button_locator)

    def place_order(self, name, country, city, credit_card, month, year):
        self.name.send_key(value=name)
        self.country.send_key(value=country)
        self.city.send_key(value=city)
        self.credit_card.send_key(value=credit_card)
        self.month.send_key(value=month)
        self.year.send_key(value=year)
        self.purchase.click()

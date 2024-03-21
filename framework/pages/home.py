from framework.components import header, items
from framework.pages import login, sign_up

login_page = login.LoginPage()
sign_up_page = sign_up.SignUpPage()


class HomePageLocators:
    header_locator = '//div[contains(@class,"navbar")]'


class HomePage(HomePageLocators):

    def __init__(self):
        super().__init__()
        self.header = header.Header(locator=self.header_locator)
        self.products = items.ItemsSection()

    def perform_login(self, username="andra@gmail.com", password="1234"):
        self.header.log_in.click()
        login_page.perform_login(username=username, pasword=password)

    def sign_up(self, email="andra@gmail.com", password="1234"):
        self.header.sign_up.click()
        sign_up_page.create_account(email=email, password=password)

    def perform_logout(self):
        self.header.log_out.click()

    def navigate_to_cart_page(self):
        self.header.cart.click()

    def select_product_with_name(self, product_name):
        count_of_products = self.products.get_total_count_of_products()
        for product in range(count_of_products):
            if product_name == self.products.associated_products[product].product_name.text:
                assert self.products.associated_products[product].product_name.click()
                return True
        return False





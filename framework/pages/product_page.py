from framework.components import header
from framework.components.items import Product
from framework.core import browser


class ProductLocators:
    product_info_locator = '//div[contains(@class,"product-deatil")]'
    header_locator = '//div[contains(@class,"navbar")]'


class ProductPage(ProductLocators):
    def __init__(self):
        super().__init__()
        self.header = header.Header(locator=self.header_locator)
        self.product = Product(locator=self.product_info_locator)

    def get_product_name(self):
        return self.product.product_name.text

    def get_product_price(self):
        return self.product.price.text

    def add_to_cart_product(self):
        import time
        self.product.add_to_cart.click()
        time.sleep(3)
        alert_modal = browser.get_current_browser().switch_to.alert
        alert_modal.accept()

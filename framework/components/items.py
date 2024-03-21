from framework.components import text_field, button, base_component
from framework.core import browser


class ItemsSectionLocators:
    product_locator = '//div[@id="tbodyid"]//div[@class="card-block"]'


class ItemsSection(ItemsSectionLocators, base_component.BaseComponent):
    def __init__(self):
        super().__init__()
        self.product = Product(locator=self.product_locator)

    @property
    def associated_products(self):
        elements_count = browser.count_elements(self.product_locator)
        return [Product(f"({self.product_locator})[{element_index}]") for element_index in
                range(1, elements_count + 1)]

    def get_total_count_of_products(self):
        return browser.count_elements(self.product_locator)


class ProductLocators:
    product_name_locator = '//*[self::h4 or self::h2]'
    product_price_locator = '//*[self::h5 or self::h3]'
    product_description_locator = '//p[@id="article"]'
    add_to_cart_button_locator = '//a[text()="Add to cart"]'



class Product(ProductLocators, base_component.BaseComponent):
    def __init__(self, locator):
        super().__init__(locator=locator)
        self.product_name = button.Button(locator=f'{self._locator}{self.product_name_locator}')
        self.price = text_field.TextField(locator=f'{self._locator}{self.product_price_locator}')
        self.description = text_field.TextField(locator=f'{self._locator}{self.product_description_locator}')
        self.add_to_cart = button.Button(locator=self.add_to_cart_button_locator)

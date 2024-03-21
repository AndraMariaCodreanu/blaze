import logging

import pytest

from framework.pages.cart import CartPage
from framework.pages.confirmation import ConfirmationPage
from framework.pages.home import HomePage
from framework.pages.place_order import PlaceOrderPage
from framework.pages.product_page import ProductPage

HOME_PAGE = HomePage()
PRODUCT_PAGE = ProductPage()
CART_PAGE = CartPage()
CONFIRMATION_PAGE = ConfirmationPage()
PLACE_ORDER_PAGE = PlaceOrderPage()
PRODUCT_NAME = ["Samsung galaxy s6",
                "Nokia lumia 1520",
                "Samsung galaxy s7",
                "Iphone 6 32gb",
                "Sony xperia z5"]

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def be_on_home_page():
    assert HOME_PAGE.header.home.click(), "Fail, Unable to navigate to home page"


@pytest.mark.functional
def test_add_to_cart_multiple_items():
    for product_name in PRODUCT_NAME:
        be_on_home_page()
        assert HOME_PAGE.select_product_with_name(
            product_name=product_name), f"product {product_name} is not in the list"
        assert product_name == PRODUCT_PAGE.product.product_name.text, \
            f"Test Failed, expected {product_name},instead got {PRODUCT_PAGE.product.product_name.text}"
        PRODUCT_PAGE.add_to_cart_product()
    HOME_PAGE.navigate_to_cart_page()
    count_of_products = CART_PAGE.cart_table.row_count
    actual_products_from_cart = []
    for row_index in range(1, count_of_products + 1):
        actual_products_from_cart.append(
            CART_PAGE.cart_table.get_cell_content_from_row_under_column(row_index, "Title"))

    print(f'found {actual_products_from_cart}')
    for product_name in PRODUCT_NAME:
        assert product_name in actual_products_from_cart, \
            f"Test Filed, expected {product_name} to b in the list of actual products from chart"


@pytest.mark.functional
def test_remove_all_items_from_cart():
    HOME_PAGE.navigate_to_cart_page()
    CART_PAGE.remove_all_items_from_table()


@pytest.mark.e2e
@pytest.mark.parametrize('product_name', PRODUCT_NAME)
def test_e2e_place_order(product_name):
    be_on_home_page()
    assert HOME_PAGE.select_product_with_name(product_name=product_name), f"product {product_name} is not in the list"
    assert product_name == PRODUCT_PAGE.product.product_name.text, \
        f"Test Failed, expected {product_name},instead got {PRODUCT_PAGE.product.product_name.text}"

    PRODUCT_PAGE.add_to_cart_product()
    HOME_PAGE.navigate_to_cart_page()
    assert product_name == CART_PAGE.cart_table.get_cell_content_from_row_under_column(1, "Title"), \
        f"Test Filed, expected {product_name},instead got {CART_PAGE.cart_table.get_cell_content_from_row_under_column(1, "Title")}"
    CART_PAGE.plac_ordr.click()
    PLACE_ORDER_PAGE.place_order(name="Andra", country="Rom", city="is", credit_card="1234", month="12", year="25")
    PLACE_ORDER_PAGE.purchase.click()
    assert CONFIRMATION_PAGE.thank_you.wait_until_is_displayed()
    CONFIRMATION_PAGE.ok.click()


@pytest.mark.e2e
def test_e2e_place_order_for_multiple_items():
    for product_name in PRODUCT_NAME:
        be_on_home_page()
        assert HOME_PAGE.select_product_with_name(
            product_name=product_name), f"product {product_name} is not in the list"
        assert product_name == PRODUCT_PAGE.product.product_name.text, \
            f"Test Failed, expected {product_name},instead got {PRODUCT_PAGE.product.product_name.text}"

        PRODUCT_PAGE.add_to_cart_product()
    HOME_PAGE.navigate_to_cart_page()
    # assert product_name == CART_PAGE.cart_table.get_cell_content_from_row_under_column(1, "Title"), \
    #     f"Test Filed, expected {product_name},instead got {CART_PAGE.cart_table.get_cell_content_from_row_under_column(1, "Title")}"
    CART_PAGE.plac_ordr.click()
    PLACE_ORDER_PAGE.place_order(name="Andra", country="Rom", city="is", credit_card="1234", month="12", year="25")
    PLACE_ORDER_PAGE.purchase.click()
    assert CONFIRMATION_PAGE.thank_you.wait_until_is_displayed()
    CONFIRMATION_PAGE.ok.click()

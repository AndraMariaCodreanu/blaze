from framework.components import table, button, base_component


class CartLocators:
    cart_table_locator = '//div[@class="table-responsive"]'
    place_order_button_locator = '//button[text()="Place Order"]'


class CartPage(CartLocators, base_component.BaseComponent):
    def __init__(self):
        super().__init__()
        self.cart_table = table.Table(locator=self.cart_table_locator)
        self.plac_ordr = button.Button(locator=self.place_order_button_locator)

    def remove_all_items_from_table(self):
        rows_count = self.cart_table.row_count
        column_index = self.cart_table.get_column_index(column_name="x")
        for index in range(1, rows_count + 1):
            self.cart_table.click_cell_remove_by_index(row_index=index, cell_index=column_index)

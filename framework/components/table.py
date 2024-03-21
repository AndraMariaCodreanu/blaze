import logging

from framework.components.base_component import BaseComponent
from framework.core import browser

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


class TableLocators:
    header_locator = "//thead//tr"
    header_cell_locator = f"{header_locator}//th"
    row_header_cell_index_locator = header_cell_locator + "[{}]"
    body_locator = "//tbody"
    row_locator = f"{body_locator}//tr"
    row_with_index_locator = row_locator + "[{}]"
    row_cell_locator = row_with_index_locator + "//td"
    row_cell_with_index_locator = row_cell_locator + ')[{}]'
    row_cell_with_index_remove_icon_locator = f"{row_cell_with_index_locator}//a"


class Table(BaseComponent, TableLocators):

    def __init__(self, locator: str):
        super().__init__(locator=locator)

    def wait_until_rows_are_displayed(self) -> bool:
        return browser.wait_until_element_is_displayed(locator=f"{self._locator}{self.row_locator}")

    @property
    def row_count(self) -> int:
        rows_count = 0
        for row_index in range(1, browser.count_elements(xpath=f"{self._locator}{self.row_locator}") + 1):
            if browser.get_text_from_element(xpath=f'{self._locator}{self.row_locator}').strip():
                rows_count += 1
            else:
                break
        return rows_count

    @property
    def header(self) -> list:
        return [x.text.strip() for x in browser.find_elements(xpath=f"{self._locator}{self.header_cell_locator}")]

    @property
    def rows(self) -> list:
        return [x.text for x in browser.find_elements(xpath=f"{self._locator}{self.row_locator}")]

    def get_cell_content_from_row_under_column(self, row_index, column_name, is_input=False):
        column_index = self.get_column_index(column_name=column_name)

        return browser.get_text_from_element(
            xpath=f"({self._locator}{self.row_cell_with_index_locator.format(row_index, column_index)}")

    def get_cell_content_by_index(self, row_index: int, cell_index: int) -> str:
        return browser.get_text_from_element(
            xpath=f"({self._locator}{self.row_cell_with_index_locator.format(row_index, cell_index)}")

    def get_column_index(self, column_name: str) -> int:
        return 1 + self.header.index(column_name.strip())

    def click_cell_remove_by_index(self, row_index: int, cell_index: int) -> bool:
        return browser.click_on_element(
            locator=f"({self._locator}{self.row_cell_with_index_remove_icon_locator.format(row_index, cell_index)}")

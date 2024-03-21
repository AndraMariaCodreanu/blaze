import datetime
import logging
import os
import sys
import time
import traceback

import pytest
from selenium.common.exceptions import NoSuchElementException, \
    StaleElementReferenceException, \
    ElementClickInterceptedException, \
    WebDriverException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.INFO)


def get_current_browser():
    """
    :rtype: Remote
    """
    try:
        pytest.BROWSER.current_window_handle
    except (AttributeError, WebDriverException) as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ex_string = '{}\n{}'.format(ex.args,
                                    traceback.format_exception(exc_type, exc_value, exc_traceback))
        pytest.exit("Browser is not opened. Exiting. Somewhere in your code there is a method "
                    "which needs the browser to be opened. {}".format(ex_string))
    return pytest.BROWSER


def add_desired_capabilities(should_open_devtools=False):
    """
    Method used to add desired capabilities
    :return: capabilities list
    """
    logger.info("Adding desired capabilities")
    capabilities = {}

    if (should_open_devtools):
        capabilities['javascriptEnabled'] = True
        capabilities['chromeOptions'] = {
            'args': ['incognito', 'start-maximized', 'disable-extensions']
        }

    return capabilities


def get_session_id():
    """
    Method used to get session ID of the browser running
    :return: session id
    """
    driver = get_current_browser()
    session_id = driver.session_id
    return session_id


def refresh_page():
    """
    Method used to refresh page
    """
    driver = get_current_browser()
    driver.refresh()


def get_element_location_once_scrolled_into_view(element):
    """
    PERFORMS A SCROLL TO ELEMENT
    :Args: element: XPath of WebElement
    Returns: dict: a dict with the x and y coordinates of an element.

    """
    try:
        if wait_until_element_is_displayed(element):
            if not isinstance(element, WebElement):
                element = find_element_by_xpath(element)
                return element.location_once_scrolled_into_view
    except WebDriverException:
        logger.info("Exception of null element")
    return dict()  # For consistency


def scroll_to(element, location="center"):
    """ Method used to scroll to a specific element by xpath
    :Args: - element: element xpath locator
           - location: Where to place the element when scrolling. Can be 'center', 'start', 'end'
    """
    driver = get_current_browser()
    try:
        if wait_until_element_is_displayed(element):
            if not isinstance(element, WebElement):
                element = find_element_by_xpath(element)
            driver.execute_script(
                'arguments[0].scrollIntoView({{behavior: "auto", block: "{}", '
                '                              inline: "center"}});'.format(location),
                element)
    except WebDriverException:
        logger.info("Exception of null element")


def is_element_displayed_on_screen(xpath, log_error=False):
    """
    Method used to check if an element is displayed
    returns: bool
    """
    try:
        driver = get_current_browser()
        wait_until_element_is_displayed(xpath)
        element_to_find = xpath
        if not isinstance(xpath, WebElement):
            element_to_find = driver.find_element("xpath", xpath)

        if element_to_find.is_displayed():
            return True
    except NoSuchElementException:
        if log_error:
            logger.error(
                "Element with xpath {} is not displayed on screen".format(xpath))
        return False


def find_element_by_xpath(xpath, timeout_seconds=10):
    """
    Method used to find an element is displayed
    returns: element
    """
    driver = get_current_browser()
    now = datetime.datetime.now()
    while True:  # Simulate a do while loop to allow 0 value for the seconds parameter
        try:
            element = driver.find_element("xpath", xpath)
            if element:
                return element
        except (NoSuchElementException, TimeoutException) as e:
            pass
        if (datetime.datetime.now() - now).total_seconds() > timeout_seconds:
            break


def find_elements(xpath, timeout_seconds=10):
    """
    Method used to find element
    return a list of elements
    """
    try:
        driver = get_current_browser()
        if wait_until_element_is_displayed(xpath, timeout_seconds, True):
            return driver.find_elements("xpath", xpath)
    except NoSuchElementException as e:
        logger.error("NoSuchElementException {}".format(e))
    return []


def get_text_from_element(xpath, timeout_seconds=20, default_value=None):
    """
    Method used to get text from an element
    :Args: - xpath: XPath of element
           - timeout: How long to wait for element to be displayed
           - default_value: Value to return in case element is not displayed on screen
    :return: str
    """
    if not wait_until_element_is_displayed(xpath, timeout_seconds):
        if default_value is not None:
            return default_value
    element = xpath
    if not isinstance(xpath, WebElement):
        element = find_element_by_xpath(xpath)
    if not element:
        return default_value
    try:
        return element.text
    except Exception as e:
        logger.error('Exception trying to get element text: {}'.format(e.args))
    return default_value


def get_element_attribute(xpath, attribute, timeout_seconds=20):
    """
    Returns attribute value of element at XPath
    :Args: - xpath: Locator for element
           - attribute: Attribute value to be retrieved
    :return: str
    """
    wait_until_element_is_displayed(xpath, timeout_seconds)
    element = find_element_by_xpath(xpath)
    if isinstance(xpath, WebElement):
        element = xpath
    return element.get_attribute(attribute)


def get_text_from_input(xpath):
    """
    Returns text value from input
    :Args: - xpath: Locator for input
    :return: str
    """
    return get_element_attribute(xpath, 'value')


def get_text_from_elements(xpath, timeout_seconds=20):
    """
    Method used to get text from elements and a list
    :Args: - xpath: locator for elements
    :return: str
    """
    wait_until_element_is_displayed(xpath, timeout_seconds)
    elements = find_elements(xpath)
    return [element.text for element in elements]


def wait_until_element_is_displayed(locator, timeout_seconds=10, multiple=False):
    """
    Method used to wait until an element is displayed
    :Args: - locator: xpath locator for element
           - timeout_seconds: time for wait
           - multiple: if true returns the list of WebElements once they are located
    :return: bool
    """
    ignored_exceptions = (
        NoSuchElementException, StaleElementReferenceException, AttributeError,
        ElementClickInterceptedException, WebDriverException,)
    try:
        driver = get_current_browser()
        if not multiple:
            if isinstance(locator, WebElement):
                ui.WebDriverWait(driver, timeout_seconds,
                                 ignored_exceptions=ignored_exceptions).until(
                    EC.visibility_of(locator))
            else:
                ui.WebDriverWait(driver, timeout_seconds,
                                 ignored_exceptions=ignored_exceptions).until(
                    EC.visibility_of_element_located((By.XPATH, locator)))
        else:
            ui.WebDriverWait(driver, timeout_seconds,
                             ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_all_elements_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        print(
            "TimeoutException:Element with locator {} is not displayed!".format(locator))
        return False
    except NoSuchElementException:
        print(
            "NoSuchElementException:Element with locator {} is not displayed!".format(locator))
        return False


def click_on_element_when_available(locator, timeout_seconds=10):
    """
    Search for a given WebDriver element and clicks it when available.
    :return: bool
    """
    now = datetime.datetime.now()
    while True:
        try:
            if find_element_by_xpath(locator, 1):
                if click_on_element(locator):
                    return True
                else:
                    get_element_location_once_scrolled_into_view(locator)
                    if click_on_element(locator):
                        return True
        except:
            pass
        if (datetime.datetime.now() - now).total_seconds() > timeout_seconds:
            break
    return False


def click_on_element(locator, timeout_seconds=20):
    """
    Method used to click on an element given an XPath locator
    :return: bool
    """
    driver = get_current_browser()
    if wait_until_element_is_displayed(locator):
        element = ui.WebDriverWait(driver, timeout_seconds).until(
            EC.element_to_be_clickable((By.XPATH, locator)))
        try:
            element.click()
            return True
        except WebDriverException:
            logger.info(
                'Unable to click element with locator {}. Trying a second time with a scrollIntoView call!'
                .format(locator))
            try:
                scroll_to(element)
                element.click()
                return True
            except WebDriverException:
                logger.info("Screenshot at {}".format(take_screenshot()))
    else:
        logger.error("Unable to find element with locator {}".format(locator))
    return False


def wait_until_element_is_not_displayed(locator, timeout_seconds=20):
    """
    Method used to wait until an element is no longer displayed
    :return: bool
    """
    try:
        driver = get_current_browser()
        ui.WebDriverWait(driver, timeout_seconds).until(
            EC.invisibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        logger.info(
            "Element with locator {} is not displayed!".format(locator))
        return False
    except NoSuchElementException:
        logger.info(
            "Element with locator {} is not displayed!".format(locator))
        return False


def send_key(locator, value, sleep_after=2, timeout_seconds=20):
    """
    Types in `value` in input field located at `locator`
    :return: bool
    """
    wait_until_element_is_displayed(locator, timeout_seconds)
    if is_element_displayed_on_screen(locator):
        elem = find_element_by_xpath(locator)
        try:
            elem.click()
            elem.clear()
        except WebDriverException:
            delete_input(locator)
        logger.info("Sending value to input: {}".format(value))
        elem.send_keys(value)
        time.sleep(sleep_after)
        return True
    return False


def delete_input(locator, timeout_seconds=20):
    """"
    Delete the text of the input that has the given locator using Backspace
    """
    if wait_until_element_is_displayed(locator, timeout_seconds):
        elem = find_element_by_xpath(locator)
        elem.send_keys(Keys.BACK_SPACE * len(elem.get_attribute('value')))


def take_screenshot(location=None):
    """
    Takes screenshot of current browser and saves it at the specified
    location
    :return: path to screenshot
    """
    results_path = os.path.abspath(get_output_dir())

    if location is None:
        location = os.path.join(results_path, 'screenshots')

    if not os.path.exists(location):
        os.makedirs(location)

    driver = get_current_browser()
    screenshot_name = "screenshot_{}.png".format(time.strftime('%d%H%M%s'))
    screenshot_location = os.sep.join([location, screenshot_name])
    driver.get_screenshot_as_file(screenshot_location)
    return screenshot_location


def get_output_dir():
    """
    Returns abstract path of the output directory
    """
    if pytest.html_path:
        return os.path.abspath(os.path.dirname(pytest.html_path))
    return os.path.abspath(os.path.curdir)


def get_current_location():
    """
    Getting current URL
    """
    driver = get_current_browser()
    return driver.current_url


def hover_over(element):
    """
    Hovers over element at xpath
    """
    driver = get_current_browser()
    if isinstance(element, str):
        webelement = find_element_by_xpath(element)
        if not webelement:
            logger.error('[hover_over]Element not found: {}'.format(element))
            return False
        element = webelement
    if not isinstance(element, WebElement):
        logger.error("Unrecognized type xpath: {}. Expected str or WebElement".format(type(element)))
        return False
    ActionChains(driver).move_to_element(element).perform()
    return True


def count_elements(xpath, timeout_seconds=10):
    """
    Method used to return the number of elements that correspond to a given xpath.
    :param xpath: xpath of elements
    :param timeout_seconds: the timeout in seconds to be set to find_elements
    :return: int
    """
    return len(find_elements(xpath, timeout_seconds))

import time
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from .tools.utils import set_timeout_to, set_timeout_to_10_seconds


def click_submit(driver: WebDriver, button_value="submit"):
    element = driver.find_element_by_css_selector(f"button[value='{button_value}']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


def click_finish_button(driver: WebDriver):
    element = driver.find_element_by_css_selector("button[value='finish']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


def click_back_link(driver: WebDriver):
    driver.find_element_by_id("back-link").click()


def element_with_css_selector_exists(driver: WebDriver, css_selector: str) -> bool:
    set_timeout_to(driver, 0)
    return_value = len(driver.find_elements_by_css_selector(css_selector)) != 0
    set_timeout_to_10_seconds(driver)
    return return_value


def element_with_id_exists(driver: WebDriver, element_id: str) -> bool:
    return element_with_css_selector_exists(driver, f"#{element_id}")


def send_keys_to_autocomplete(driver: WebDriver, element_id: str, keys: str):
    element = driver.find_element_by_id(element_id)
    element.send_keys(keys)

    # Tab away from element and wait
    element.send_keys(Keys.TAB)
    time.sleep(1)


def send_tokens_to_token_bar(driver: WebDriver, element_selector: str, tokens: List[str]):
    element = driver.find_element_by_css_selector(element_selector)

    for token in tokens:
        element.send_keys(token)
        element.send_keys(Keys.ENTER)

    # Tab away from element and wait
    element.send_keys(Keys.TAB)
    time.sleep(1)


def try_open_filters(driver: WebDriver):
    if not driver.find_element_by_class_name("lite-filter-bar").is_displayed():
        driver.find_element_by_id("show-filters-link").click()


def get_table_rows(driver: WebDriver, table_selector: str = "table", raise_exception_if_empty=False):
    selector = f"{table_selector} tbody tr"
    rows = driver.find_elements_by_css_selector(selector)

    if raise_exception_if_empty and not rows:
        raise NoSuchElementException(f"No rows returned with selector: {selector}")

    return rows


def click_next_page(driver: WebDriver):
    driver.find_element_by_id("link-next-page").click()

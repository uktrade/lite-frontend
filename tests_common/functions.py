import time

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


def enter_value(driver: WebDriver, element_id, value):
    driver.find_element_by_id(element_id).send_keys(value)

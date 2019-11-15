from selenium.webdriver.remote.webdriver import WebDriver

from shared.tools.utils import set_timeout_to, set_timeout_to_10_seconds


def click_submit(driver: WebDriver):
    element = driver.find_element_by_css_selector("button[value='submit']")
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

import time
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def click_submit(driver: WebDriver):
    element = driver.find_element(by=By.CSS_SELECTOR, value='.govuk-button[type*="submit"]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


def click_finish_button(driver: WebDriver):
    element = driver.find_element(by=By.CSS_SELECTOR, value="button[value='finish']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


def click_back_link(driver: WebDriver):
    driver.find_element(by=By.ID, value="back-link").click()


def click_continue_link(driver: WebDriver):
    driver.find_element(by=By.LINK_TEXT, value="Continue").click()


def click_save_and_continue_link(driver: WebDriver):
    driver.find_element(by=By.LINK_TEXT, value="Save and continue").click()


def element_with_css_selector_exists(driver: WebDriver, css_selector: str) -> bool:
    driver.implicitly_wait(0)
    return_value = len(driver.find_elements(by=By.CSS_SELECTOR, value=css_selector)) != 0
    driver.implicitly_wait(60)
    return return_value


def element_with_id_exists(driver: WebDriver, element_id: str) -> bool:
    return element_with_css_selector_exists(driver, f"#{element_id}")


def send_keys_to_autocomplete(driver: WebDriver, element_id: str, keys: str):
    element = driver.find_element(by=By.ID, value=element_id)
    element.send_keys(keys)

    # Tab away from element and wait
    element.send_keys(Keys.TAB)
    time.sleep(1)


def send_tokens_to_token_bar(driver: WebDriver, element_selector: str, tokens: List[str]):
    element = driver.find_element(by=By.CSS_SELECTOR, value=element_selector)

    for token in tokens:
        element.send_keys(token)
        element.send_keys(Keys.ENTER)

    # Tab away from element and wait
    element.send_keys(Keys.TAB)
    time.sleep(1)


def select_multi_select_options(driver: WebDriver, element_selector: str, options: List[str]):
    for option in options:
        element = driver.find_element(by=By.CSS_SELECTOR, value=element_selector)
        element.send_keys(option)
        element.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f"//span[@class='selected-options__option-text' and contains(text(), '{option}')]")
            ),
        )


def click_apply_filters(driver: WebDriver):
    driver.find_element(by=By.ID, value="button-apply-filters").click()


def open_case_filters(driver: WebDriver):
    if not driver.find_element(by=By.CLASS_NAME, value="case-filters").is_displayed():
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, "show-filters-link"))
        ).click()
        WebDriverWait(driver, 30).until(
            expected_conditions.element_to_be_clickable((By.ID, "accordion-case-filters"))
        ).click()


def try_open_filters(driver: WebDriver):
    if not driver.find_element(by=By.CLASS_NAME, value="lite-filter-bar").is_displayed():
        WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, "show-filters-link"))
        ).click()


def get_table_rows(driver: WebDriver, table_selector: str = "table", raise_exception_if_empty=False):
    selector = f"{table_selector} tbody tr"
    rows = driver.find_elements_by_css_selector(selector)

    if raise_exception_if_empty and not rows:
        raise NoSuchElementException(f"No rows returned with selector: {selector}")

    return rows


def click_next_page(driver: WebDriver):
    driver.find_element(by=By.ID, value="link-next-page").click()


def select_report_summary_subject_and_fill(driver, subject):
    suggestion_input_autocomplete = driver.find_element(by=By.ID, value="_report_summary_subject")
    suggestion_input_autocomplete.send_keys(subject)
    WebDriverWait(driver, 30).until(
        expected_conditions.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".lite-autocomplete__menu--visible #_report_summary_subject__option--0"),
            subject,
        )
    )
    suggestion_input_autocomplete.send_keys(Keys.ARROW_DOWN)
    driver.find_element(by=By.XPATH, value="//body").click()


def select_report_summary_prefix_and_fill(driver, prefix):
    suggestion_input_autocomplete = driver.find_element(by=By.ID, value="_report_summary_prefix")
    suggestion_input_autocomplete.send_keys(prefix)
    WebDriverWait(driver, 30).until(
        expected_conditions.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".lite-autocomplete__menu--visible #_report_summary_prefix__option--0"),
            prefix,
        )
    )
    suggestion_input_autocomplete.send_keys(Keys.ARROW_DOWN)
    driver.find_element(by=By.XPATH, value="//body").click()


def click_regime_none(driver: WebDriver):
    driver.find_element(
        By.XPATH,
        "//input[@name='regimes' and @value='NONE']",
    ).click()

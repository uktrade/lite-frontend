from time import sleep

from ..tools.helpers import page_is_ready, menu_is_visible

TIMEOUT_LIMIT = 60  # How many attempts to wait for the function to return True
FUNCTION_RETRY_INTERVAL = 1  # How frequently in seconds the function should be checked


def wait_for_function(callback_function, **kwargs):
    time_no = 0
    while time_no < TIMEOUT_LIMIT:
        if callback_function(**kwargs):
            return True
        sleep(FUNCTION_RETRY_INTERVAL)
        time_no += FUNCTION_RETRY_INTERVAL
    return False


def is_download_link_present(driver):
    driver.refresh()
    return "Download" in driver.find_element_by_tag_name("body").text


def element_is_present(driver, _id):
    driver.refresh()
    return bool(driver.find_elements_by_id(_id))


def wait_for_download_button(driver):
    return wait_for_function(is_download_link_present, driver=driver)


def wait_for_element(driver, _id):
    return wait_for_function(element_is_present, driver=driver, _id=_id)


def wait_until_page_is_loaded(driver):
    return wait_for_function(page_is_ready, driver=driver)


def wait_until_menu_is_visible(driver):
    return wait_for_function(menu_is_visible, driver=driver)

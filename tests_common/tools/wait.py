from time import sleep

from .helpers import page_is_ready, menu_is_visible

from pages.shared import Shared

# How many attempts to wait for the function to return True
timeout_limit = 60
# How frequently in seconds the function should be checked
function_retry_interval = 1


def wait_for_function(callback_function, **kwargs):
    time_no = 0
    while time_no < timeout_limit:
        if callback_function(**kwargs):
            return True
        sleep(function_retry_interval)
        time_no += function_retry_interval
    return False


def download_link_is_present(driver, page):
    driver.refresh()
    return "Download" in Shared(driver).get_text_of_body()


def element_is_present(driver, id):
    driver.refresh()
    return bool(driver.find_elements_by_id(id))


def wait_for_download_button(driver, page):
    return wait_for_function(download_link_is_present, driver=driver, page=page)


def wait_for_element(driver, id):
    return wait_for_function(element_is_present, driver=driver, id=id)


def wait_until_page_is_loaded(driver):
    return wait_for_function(page_is_ready, driver=driver)


def wait_until_menu_is_visible(driver):
    return wait_for_function(menu_is_visible, driver=driver)

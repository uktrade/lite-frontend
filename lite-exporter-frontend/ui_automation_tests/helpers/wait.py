import time

# How many attempts to wait for the function to return True
from pages.shared import Shared

timeout_limit = 20
# How frequently in seconds the function should be checked
function_retry_interval = 1


def wait_for_function(func, **kwargs):
    time_no = 0
    while time_no < timeout_limit:
        if func(**kwargs):
            return True
        time.sleep(function_retry_interval)
        time_no += function_retry_interval
    return False


def wait_for_document(func, draft_id):
    return wait_for_function(func, draft_id=draft_id)


def wait_for_ultimate_end_user_document(func, draft_id, ultimate_end_user_id):
    return wait_for_function(func, draft_id=draft_id,
                             ultimate_end_user_id=ultimate_end_user_id)


def download_link_is_present(driver):
    driver.refresh()
    shared = Shared(driver)
    latest_ueu_links = [link.text for link in shared.get_links_of_table_row(-1)]
    return 'Download' in latest_ueu_links


def element_is_present(driver, id):
    driver.refresh()
    return bool(driver.find_elements_by_id(id))


def wait_for_download_button(driver):
    return wait_for_function(download_link_is_present, driver=driver)


def wait_for_element(driver, id):
    return wait_for_function(element_is_present, driver=driver, id=id)

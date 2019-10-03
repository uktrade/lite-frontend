import time

from shared.tools.helpers import page_is_ready, menu_is_visible

# How many attempts to wait for the function to return True
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


def wait_for_document(func, draft_id, base_url, export_headers):
    return wait_for_function(func, draft_id=draft_id,
                             base_url=base_url, export_headers=export_headers)


def wait_for_ultimate_end_user_document(func, draft_id, ultimate_end_user_id, base_url, export_headers):
    return wait_for_function(func, draft_id=draft_id,
                             ultimate_end_user_id=ultimate_end_user_id,
                             base_url=base_url, export_headers=export_headers)


def wait_for_third_party_document(func, draft_id, third_party_id, base_url, export_headers):
    return wait_for_function(func, draft_id=draft_id,
                             third_party_id=third_party_id,
                             base_url=base_url, export_headers=export_headers)


def wait_for_additional_document(func, draft_id, document_id, base_url, export_headers):
    return wait_for_function(func, draft_id=draft_id,
                             document_id=document_id,
                             base_url=base_url, export_headers=export_headers)


def download_link_is_present(driver, page):
    driver.refresh()
    latest_ueu_links = [link.text for link in page.get_links_of_table_row(-1)]
    return 'Download' in latest_ueu_links


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

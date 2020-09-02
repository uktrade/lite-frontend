from django.utils import timezone
from os import path, makedirs, chmod, pardir
from re import search
from time import sleep

from allure import attach, attachment_type
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django.conf import settings


now = timezone.localtime().isoformat()

screen_dir = path.join(settings.BASE_DIR, "ui_tests/screenshots")

PAGE_LIMIT = 100


def get_current_date_time_string():
    return timezone.localtime().strftime("%Y/%m/%d %H:%M:%S:%f")


def get_formatted_date_time_m_d_h_s():
    return timezone.localtime().strftime("%m%d%H%M%S")


def get_formatted_date_time_y_m_d_h_s():
    return timezone.localtime().strftime("%Y%m%d%H%M%S")


def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length // len(string_to_expand)) + 1))[:length]


def screen_path():
    if not path.exists(screen_dir):
        makedirs(screen_dir)
    return screen_dir


def save_screenshot(driver, name):
    location = path.join(screen_path(), str(name) + ".png")
    driver.get_screenshot_as_file(location)
    attach(
        driver.get_screenshot_as_png(), now, attachment_type=attachment_type.PNG,
    )


def find_element(driver, by_type, locator):
    delay = 2  # seconds
    try:
        return WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_type, locator)))
    except TimeoutException:
        print("element {} was not found".format(locator))


def find_element_by_href(driver, href):
    return driver.find_element_by_css_selector('[href="' + href + '"]')


def is_element_present(driver, how, what):
    """
    Helper method to confirm the presence of an element on page
    :params how: By locator type
    :params what: locator value
    """
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def click(driver, by_type, locator):
    el = find_element(driver, by_type, locator)
    el.click()


def type_text(driver, text, by_type, locator):
    el = find_element(driver, by_type, locator)
    el.click()
    el.send_keys(text)


def get_text(driver, by_type, locator):
    el = find_element(driver, by_type, locator)
    return el.text


def scroll_down_page(driver, x, y):
    driver.execute_script("window.scrollTo(" + str(x) + ", " + str(y) + ")")


def scroll_to_bottom_of_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


def scroll_to_right_of_page(driver):
    driver.execute_script("window.scrollBy(document.body.scrollWidth, 0)")


def highlight(element):
    """
    Highlights (blinks) a Selenium Webdriver element
    """
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)

    original_style = element.get_attribute("style")
    apply_style("background: yellow; border: 2px solid red;")
    sleep(0.8)
    apply_style(original_style)


def get_element_index_by_text(elements, text: str, complete_match=True):
    """
    Loops through the list of elements, checks if the text is equal or in
    text and returns the index of it if so
    """
    for i in range(0, len(elements)):
        if complete_match:
            if elements[i].text == text:
                return i
        else:
            if text in elements[i].text:
                return i
    return -1


def get_coordinates_of_element_by_id(driver, selector):
    return driver.find_element_by_id(selector).location


def get_size_of_element_by_id(driver, selector):
    return driver.find_element_by_id(selector).size


def scroll_to_element_below_header_by_id(driver, selector):
    size_of_header = get_size_of_element_by_id(driver, "app-header")
    location_of_wanted_element = get_coordinates_of_element_by_id(driver, selector)
    required_height = location_of_wanted_element["y"] - size_of_header["height"]
    driver.execute_script(
        "window.scrollTo(" + str(location_of_wanted_element["x"]) + ", " + str(required_height) + ");"
    )


def scroll_to_element_by_id(driver, element_id):
    driver.execute_script("document.getElementById('" + element_id + "').scrollIntoView(true);")


def search_for_correct_date_regex_in_element(element):
    return search(
        "([0-9]{1,2}):([0-9]{2})(am|pm) ([0-9][0-9]) (January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]{4,})",
        element,
    )


def get_formatted_date_time_h_m_pm_d_m_y():
    time = timezone.localtime().strftime("%I:%M%p %d %B %Y").replace("PM", "pm").replace("AM", "am")
    if time[0] == "0":
        time = time[1:]
    return time


def get_unformatted_date_time():
    return timezone.localtime()


def get_formatted_date_time_d_h_m_s():
    return str(timezone.localtime().strftime("%d%H%M%S"))


def page_is_ready(driver):
    return driver.execute_script("return document.readyState") == "complete"


def find_paginated_item_by_id(id, driver):
    driver.implicitly_wait(0)
    current_page = 1
    while True:
        element_to_find = driver.find_elements_by_id(id)
        if element_to_find:
            element_is_found = element_to_find[0]
            break
        elif current_page == PAGE_LIMIT:
            assert False, f"'{id}' couldn't be found across {current_page} pages"
        else:
            current_page += 1
            try:
                driver.find_element_by_id(f"page-{current_page}").click()
            except NoSuchElementException:
                pass
    driver.implicitly_wait(60)
    assert element_is_found, f"'{id}' couldn't be found across {current_page} pages"
    return element_is_found


def paginated_item_exists(item_id, driver, exists=True):
    driver.implicitly_wait(0)
    current_page = 1
    while True:
        element_to_find = driver.find_elements_by_id(item_id)
        if element_to_find:
            element_is_found = element_to_find[0]
            break
        elif current_page == PAGE_LIMIT:
            element_is_found = False
            break
        else:
            current_page += 1
            try:
                driver.find_element_by_id(f"page-{current_page}").click()
            except NoSuchElementException:
                element_is_found = False
                break
    driver.implicitly_wait(60)
    return bool(element_is_found) == exists


def paginated_item_exists_by_css(css, driver, exists=True):
    driver.implicitly_wait(0)
    current_page = 1
    while True:
        element_to_find = driver.find_elements_by_css_selector(css)
        if element_to_find:
            element_is_found = element_to_find[0]
            break
        elif current_page == PAGE_LIMIT:
            element_is_found = False
            break
        else:
            current_page += 1
            try:
                driver.find_element_by_id(f"page-{current_page}").click()
            except NoSuchElementException:
                element_is_found = False
                break
    driver.implicitly_wait(60)
    return bool(element_is_found) == exists


def get_text_of_multi_page_table(css_selector, driver):
    driver.implicitly_wait(0)
    text = ""
    current_page = 1
    while True:
        text += driver.find_element_by_css_selector(css_selector).text
        current_page += 1
        try:
            driver.find_element_by_id(f"page-{current_page}").click()
        except NoSuchElementException:
            break
    driver.implicitly_wait(60)
    return text


def strip_special_characters(string):
    return "".join(e for e in string if e.isalnum())


def get_current_date_time(format_date_time=True):
    date_time = timezone.localtime()
    if not format_date_time:
        return date_time
    return strip_special_characters(str(date_time))


def get_element_row_text_from_table(elements, text_to_search_on):
    element_index = get_element_index_by_text(elements, text_to_search_on, complete_match=False)
    # Element index -1 means an element with the given text was not found
    if element_index != -1:
        return elements[element_index].text

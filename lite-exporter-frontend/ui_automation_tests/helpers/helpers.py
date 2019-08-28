import allure
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time

now = datetime.now().isoformat()
path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
screen_dir = os.path.join(path, "screenshot", str(now))


def get_current_date_time_string():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")

def get_formatted_date_time_h_m_pm_d_m_y():
    time = datetime.now().strftime("%I:%M%p %d %B %Y").replace("PM", "pm").replace(
        "AM", "am")
    if time[0] == "0":
        time = time[1:]
    return time

def get_unformatted_date_time():
    return datetime.now()


def get_formatted_date_time_m_d_h_s():
    return datetime.now().strftime("%m%d%H%M%S")

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]


def screen_path():
    global screen_dir
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir)
        os.chmod(screen_dir, 0o644)
    return screen_dir


def remove_special_characters(text):
    # text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', '\ / : * ? " < > |'))
    return text


def save_screenshot(driver, name):
    _name = remove_special_characters(name)
    driver.get_screenshot_as_file(os.path.join(screen_path(), _name + '-' + now + ".png"))
    allure.attach(driver.get_screenshot_as_png(), name=_name + "-" + now, attachment_type=allure.attachment_type.PNG)


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


def highlight(element):
    """
    Highlights (blinks) a Selenium Webdriver element
    """
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.8)
    apply_style(original_style)


def get_element_by_text(elements, text: str):
    """
    Loops through the list of elements, checks if the text is equal to
    text and returns the element if so
    """
    for element in elements:
        if element == text:
            return element


def get_element_index_by_text(elements, text: str):
    """
    Loops through the list of elements, checks if the text is equal to
    text and returns the index of it if so
    """
    no = 0
    element_number = -1
    while no < len(elements):
        if elements[no].text == text:
            element_number = no
            break
        no += 1

    return element_number


def get_element_index_by_partial_text(elements, text: str):
    """
    Loops through the list of elements, checks if the text is equal to
    text and returns the index of it if so
    """
    no = 0
    element_number = -1
    while no < len(elements):
        if text in elements[no].text:
            element_number = no
            break
        no += 1

    return element_number


def split_and_replace_date_time(date):
    return date.split(':')[1].replace('am', '').replace('pm', '')


def replace_pm_am_datetime(date):
    return date.replace('am', '').replace('pm', '')

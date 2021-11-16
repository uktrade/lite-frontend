import os.path
from os.path import abspath, relpath, dirname

from pytest_bdd import given, when, then, parsers

RESOURCES_PATH = os.path.join(dirname(__file__), "resources")


def get_elements_by_visible_text(driver, text):
    return driver.find_elements_by_xpath(f"//*[contains(text(),'{text}')]")


def get_element_by_visible_text(driver, text):
    found_elements = get_elements_by_visible_text(driver, text)
    if not found_elements:
        raise Exception(f"No element found with text '{text}'")
    if len(found_elements) > 1:
        raise Exception(f"Too many elements found with text '{text}'. Be more specific")
    element = found_elements[0]
    assert element.text == text
    return element


def get_child_by_visible_text(driver, parent_visible_text, child_visible_text):
    xpath = f"//*[contains(text(), '{parent_visible_text}')]/parent::*//*[contains(text(), '{child_visible_text}')]"
    found_elements = driver.find_elements_by_xpath(xpath)
    if not found_elements:
        raise Exception(f"No element found with xpath '{xpath}'")
    if len(found_elements) > 1:
        raise Exception(f"Too many elements found with xpath '{xpath}'. Be more specific")
    element = found_elements[0]
    assert element.text == child_visible_text
    return element


# ------------------------------------------------ Steps ---------------------------------------------------------------


@then("debug")
def then_debug(context):
    import IPython; IPython.embed(using=False)


@when("debug")
def when_debug(context):
    import IPython; IPython.embed(using=False)


@when(parsers.parse("I select \"{selection_text}\" when asked \"{question_text}\""))
def select_from_radio(selection_text, question_text, driver, context):
    element = get_child_by_visible_text(driver, question_text, selection_text)
    element.click()


@when(parsers.parse("I attach \"{file_name}\" into \"{element_id}\""))
def attach_file(file_name, element_id, driver, context):
    element = driver.find_element_by_id(element_id)
    file_path = os.path.join(RESOURCES_PATH, file_name)
    element.send_keys(file_path)


@when(parsers.parse("I click \"{text}\""))
def click_element(text, driver, context):
    element = get_element_by_visible_text(driver, text)
    element.click()


@then(parsers.parse("I see \"{text}\""))
def see_text(text, driver, context):
    if not get_elements_by_visible_text(driver, text):
        raise Exception(f"Expected at least one element with text '{text}', got 0.")

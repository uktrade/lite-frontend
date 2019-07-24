from pytest_bdd import scenarios, given, when, then, parsers, scenarios
import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.shared import Shared

from pages.flags_pages import FlagsPages

scenarios('../features/flags.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@then('I see the flag in the flag list')
def see_flag_in_list(driver, context):
    flag_name = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.flag_name + "')]]")
    assert flag_name.is_displayed()


@when('I add an existing flag name')
def add_existing_flag(driver, context):
    flags_pages = FlagsPages(driver)
    shared = Shared(driver)
    flags_pages.click_add_a_flag_button()
    flags_pages.enter_flag_name(context.flag_name)
    shared.click_submit()


@when('I edit my flag')
def edit_existing_flag(driver, context):
    elements = driver.find_elements_by_css_selector("td a")
    no = 0
    while no < len(elements):
        if elements[no].text == context.flag_name:
            element_number = no
        no += 1

    elements[element_number + 2].click()
    flags_pages = FlagsPages(driver)
    context.flag_name = str(context.flag_name)[:12] + "edited"
    flags_pages.enter_flag_name(context.flag_name)
    driver.find_element_by_css_selector("[type*='submit']").click()


@when('I count the number of active flags')
def count_active_flags(driver, context):
    number_of_active_flags = len(driver.find_elements_by_xpath('//*[text()[contains(.,"Active")]]'))
    number_of_deactivated_flags = len(driver.find_elements_by_xpath('//*[text()[contains(.,"Deactivated")]]'))
    context.original_number_of_active_flags = number_of_active_flags
    context.original_number_of_deactivated_flags = number_of_deactivated_flags


@when('I deactivate the first active flag')
def deactivate_first_active_flag(driver):
    driver.find_element_by_css_selector("[href*='edit/deactivate/']").click()
    Shared(driver).click_submit()


@when('I click include deactivated')
def click_include_deactivated(driver):
    if len(driver.find_elements_by_css_selector("[href*='flags/all/']")) == 1:
        driver.find_element_by_css_selector("[href*='flags/all/']").click()


@when('I click include reactivated if displayed')
def click_include_deactivated(driver):
    if len(driver.find_element_by_css_selector("[href*='/flags/active/']")) == 1:
        driver.find_element_by_css_selector("[href*='/flags/active/']").click()


@then('I see one less active flags')
def i_see_one_less_active_flag(driver, context):
    number_of_active_flags = len(driver.find_elements_by_xpath('//*[text()[contains(.,"Active")]]'))
    number_of_deactivated_flags = len(driver.find_elements_by_xpath('//*[text()[contains(.,"Deactivated")]]'))

    assert context.original_number_of_active_flags - number_of_active_flags == 1
    assert context.original_number_of_deactivated_flags - number_of_deactivated_flags == -1


@when('I reactivate the first deactivated flag')
def reactivate_first_deactivated_flag(driver):
    driver.find_element_by_css_selector("[href*='edit/reactivate/']").click()
    Shared(driver).click_submit()


@then('I see the original number of active flags')
def i_see_the_original_number_of_active_flags(driver, context):
    number_of_active_flags = len(driver.find_elements_by_xpath('//*[text()[contains(.,"Active")]]'))
    number_of_deactivated_flags = len(driver.find_elements_by_xpath('//*[text()[contains(.,"Deactivated")]]'))

    assert context.original_number_of_active_flags == number_of_active_flags
    assert context.original_number_of_deactivated_flags == number_of_deactivated_flags

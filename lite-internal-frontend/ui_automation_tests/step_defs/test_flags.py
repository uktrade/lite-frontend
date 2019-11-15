from pytest_bdd import when, then, parsers, scenarios
import shared.tools.helpers as utils
from pages.header_page import HeaderPage
from pages.shared import Shared

from pages.flags_pages import FlagsPages

scenarios("../features/flags.feature", strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@then("I see the flag in the flag list")
def see_flag_in_list(driver, context):
    assert context.flag_name in Shared(driver).get_text_of_table()


@when("I add an existing flag name")
def add_existing_flag(driver, context):
    flags_pages = FlagsPages(driver)
    shared = Shared(driver)
    flags_pages.click_add_a_flag_button()
    flags_pages.enter_flag_name(context.flag_name)
    shared.click_submit()


@when("I edit my flag")
def edit_existing_flag(driver, context):
    elements = Shared(driver).get_links_in_cells_in_table()
    element_number = utils.get_element_index_by_text(elements, context.flag_name)
    elements[element_number + 2].click()
    flags_pages = FlagsPages(driver)
    context.flag_name = str(context.flag_name)[:18] + " 1"
    flags_pages.enter_flag_name(context.flag_name)
    Shared(driver).click_submit()


@when("I count the number of active flags")
def count_active_flags(driver, context):
    context.original_number_of_active_flags = FlagsPages(driver).get_size_of_active_flags()
    context.original_number_of_deactivated_flags = FlagsPages(driver).get_size_of_inactive_flags()


@when("I deactivate the first active flag")
def deactivate_first_active_flag(driver):
    FlagsPages(driver).click_on_deactivate_flag()
    Shared(driver).click_submit()


@when("I click include deactivated")
def click_include_deactivated(driver):
    flags = FlagsPages(driver)
    driver.set_timeout_to(0)
    if flags.is_include_deactivated_button_displayed():
        flags.click_include_deactivated_flags()
    driver.set_timeout_to_10_seconds()


@when("I click include reactivated if displayed")
def click_include_reactivated(driver):
    flags = FlagsPages(driver)
    driver.set_timeout_to(0)
    if flags.is_include_reactivated_button_displayed():
        flags.click_include_reactivated_flags()
    driver.set_timeout_to_10_seconds()


@then("I see one less active flags")
def i_see_one_less_active_flag(driver, context):
    flags = FlagsPages(driver)
    number_of_active_flags = flags.get_size_of_active_flags()
    number_of_deactivated_flags = flags.get_size_of_inactive_flags()

    assert context.original_number_of_active_flags - number_of_active_flags == 1, "There is not one less flag"
    assert (
        context.original_number_of_deactivated_flags - number_of_deactivated_flags == -1
    ), "There is not one less deactivated flag"


@when("I reactivate the first deactivated flag")
def reactivate_first_deactivated_flag(driver):
    FlagsPages(driver).click_on_reactivate_flag()
    Shared(driver).click_submit()


@then("I see the original number of active flags")
def i_see_the_original_number_of_active_flags(driver, context):
    flags = FlagsPages(driver)
    number_of_active_flags = flags.get_size_of_active_flags()
    number_of_deactivated_flags = flags.get_size_of_inactive_flags()

    assert context.original_number_of_active_flags == number_of_active_flags, "There is not equal flags to before"
    assert (
        context.original_number_of_deactivated_flags == number_of_deactivated_flags
    ), "There is not equal deactivated flags to before"


@when(parsers.parse('I add a flag called "{flag_name}" at level "{flag_level}"'))
def add_a_flag(driver, flag_name, flag_level, context):
    flags_page = FlagsPages(driver)
    flags_page.click_add_a_flag_button()
    flags_page.enter_flag_name(flag_name)
    flags_page.select_flag_level(flag_level)
    Shared(driver).click_submit()


@when("I add a flag called UAE at level Case")
def add_a_uae_flag(driver, context, add_uae_flag):
    pass

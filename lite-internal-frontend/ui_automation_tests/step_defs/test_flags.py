from pytest_bdd import when, then, scenarios, parsers

import shared.tools.helpers as utils
from pages.add_edit_flag import AddEditFlagPage
from pages.advice import FinalAdvicePage
from pages.flags_list_page import FlagsListPage
from pages.shared import Shared
from shared import functions

scenarios("../features/flags.feature", strict_gherkin=False)


@when(parsers.parse('I add a new flag with blocking approval set to "{blocks_approval}"'))
def add_flag(driver, context, blocks_approval):
    add_edit_flag_page = AddEditFlagPage(driver)
    context.flag_name = "UAE" + utils.get_formatted_date_time_d_h_m_s()

    FlagsListPage(driver).click_add_a_flag_button()

    add_edit_flag_page.enter_name(context.flag_name)
    add_edit_flag_page.select_level("Case")
    add_edit_flag_page.select_colour("orange")
    add_edit_flag_page.enter_label("Easy to Find")
    add_edit_flag_page.enter_priority(0)
    add_edit_flag_page.enter_blocking_approval(blocks_approval)

    Shared(driver).click_submit()


@when("I edit the flag I just made")
def edit_existing_flag(driver, context):
    flags_list_page = FlagsListPage(driver)
    add_edit_flag_page = AddEditFlagPage(driver)
    flags_list_page.click_edit_link()

    context.flag_name = "Edited flag" + utils.get_formatted_date_time_d_h_m_s()
    add_edit_flag_page.enter_name(context.flag_name)
    add_edit_flag_page.select_colour("red")
    add_edit_flag_page.enter_label("Hard to Find")
    add_edit_flag_page.enter_priority(1)

    Shared(driver).click_submit()


@then("I see the flag in the flag list")
def i_see_flag_in_list(driver, context):
    FlagsListPage(driver).filter_by_name(context.flag_name)
    assert context.flag_name in Shared(driver).get_text_of_table()


@when("I deactivate the flag")
def deactivate_flag(driver, context):
    FlagsListPage(driver).click_deactivate_link()
    functions.click_submit(driver, "Deactivated")


@when("I click only show deactivated")
def only_show_deactivated_flags(driver, context):
    FlagsListPage(driver).click_only_show_deactivated()


@when("I reactivate the flag")
def reactivate_flag(driver, context):
    FlagsListPage(driver).click_reactivate_link()
    functions.click_submit(driver, "Active")


@then("I cannot finalise the case due to the blocking flag")
def cannot_finalise_blocking_flag(driver, context):
    final_advice = FinalAdvicePage(driver)
    assert not final_advice.can_finalise()
    assert context.flag_name in final_advice.get_blocking_flags_text()

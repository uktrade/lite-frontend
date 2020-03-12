from pytest_bdd import when, then, scenarios, parsers
import shared.tools.helpers as utils
from pages.shared import Shared

from ui_automation_tests.pages.flagging_rules_pages import FlaggingRulePages

scenarios("../features/flagging_rules.feature", strict_gherkin=False)


@when("I go to flagging rules list")
def go_to_flagging_rules(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/flags/rules/")


@then("I see the flagging rule in the flag list")
def see_flag_in_list(driver, context):
    assert utils.find_paginated_item_by_id(context.flag_id, driver)


@when("I click include deactivated")
def click_include_deactivated(driver):
    FlaggingRulePages(driver).click_include_deactivated()
    FlaggingRulePages(driver).click_apply_filters_button()


@when(parsers.parse('I add a flagging rule of type "{type}", with condition "{condition}", and flag'))
def create_flagging_rule(driver, context, type, condition):
    flagging_rules_page = FlaggingRulePages(driver)
    flagging_rules_page.create_new_flagging_rule()

    flagging_rules_page.select_flagging_rule_type(type)

    Shared(driver).click_submit()

    if type == "Case":
        flagging_rules_page.select_case_type(condition)
    elif type == "Destination":
        flagging_rules_page.enter_country(condition)
    elif type == "Good":
        flagging_rules_page.enter_control_list(condition)

    flagging_rules_page.select_flag(context.flag_name)

    Shared(driver).click_submit()


@when(parsers.parse('I edit my "{type}" flagging rule with condition "{condition}"'))
def edit_flagging_rule(driver, context, condition):
    flagging_rules_page = FlaggingRulePages(driver)

    # select edit for my flagging rule
    utils.find_paginated_item_by_id(context.flag_id, driver).find_element_by_xpath("..").find_element_by_link_text(
        "Edit"
    ).click()

    if type == "Case":
        flagging_rules_page.select_case_type(condition)
    elif type == "Destination":
        flagging_rules_page.select_country(condition)
    elif type == "Good":
        flagging_rules_page.enter_control_list(condition)

    Shared(driver).click_submit()


@then(parsers.parse('I see the flagging rule in the list as "{status}"'))
def create_flagging_rule(driver, context, status):
    assert status in utils.find_paginated_item_by_id(context.flag_id, driver).find_element_by_xpath("..").text


@when("I deactivate my flagging rule")
def deactivate_first_active_flag(driver, context):
    row = utils.find_paginated_item_by_id(context.flag_id, driver).find_element_by_xpath("..")
    FlaggingRulePages(driver).click_on_deactivate_flag(row)
    FlaggingRulePages(driver).click_confirm_deactivate_activate()
    Shared(driver).click_submit()

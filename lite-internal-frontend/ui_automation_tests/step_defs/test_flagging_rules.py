from pytest_bdd import when, then, scenarios, parsers, given
import shared.tools.helpers as utils
from pages.shared import Shared
from shared import functions

from ui_automation_tests.pages.flagging_rules_pages import FlaggingRulePages

scenarios("../features/flagging_rules.feature", strict_gherkin=False)


@when("I go to flagging rules list")
def go_to_flagging_rules(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/flags/rules/")


@then(parsers.parse('I see the flagging rules in the flag list as "{status}"'))
def see_flag_in_list(driver, context, status):
    for level in context.flags:
        assert status in driver.find_element_by_id(context.flags[level]["id"]).text


@when("I click include deactivated")
def click_include_deactivated(driver):
    FlaggingRulePages(driver).click_include_deactivated()
    functions.click_apply_filters(driver)


@when(
    parsers.parse(
        'I add a goods flagging rule with condition "{condition}", flag and answer "{answer}" for only apply to verified goods'
    )
)
def create_goods_flagging_rule(driver, context, condition, answer):
    flagging_rules_page = FlaggingRulePages(driver)
    flagging_rules_page.create_new_flagging_rule()
    flagging_rules_page.select_flagging_rule_type("Good")

    Shared(driver).click_submit()

    flagging_rules_page.enter_control_list(condition)
    flagging_rules_page.select_is_for_verified_goods_only(answer)
    flagging_rules_page.select_flag(context.flags["Good"]["name"])

    Shared(driver).click_submit()


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

    flagging_rules_page.select_flag(context.flags[type]["name"])

    Shared(driver).click_submit()


@when(parsers.parse('I edit my "{type}" flagging rule with condition "{condition}"'))
def edit_flagging_rule(driver, context, condition):
    flagging_rules_page = FlaggingRulePages(driver)
    row = driver.find_element_by_id(context.flag_id)

    # select edit for my flagging rule
    flagging_rules_page.click_on_edit_for_element(row)

    if type == "Case":
        flagging_rules_page.select_case_type(condition)
    elif type == "Destination":
        flagging_rules_page.enter_country(condition)
    elif type == "Good":
        flagging_rules_page.enter_control_list(condition)

    Shared(driver).click_submit()


@then(parsers.parse('I see the flagging rule in the list as "{status}"'))
def create_flagging_rule(driver, context, status):
    assert status in driver.find_element_by_id(context.flag_id).text


@when("I deactivate all my new flagging rules")
def deactivate_first_active_flag(driver, context, internal_url):
    for level in context.flags:
        row = driver.find_element_by_id(context.flags[level]["id"])
        FlaggingRulePages(driver).click_on_deactivate_flag(row)
        FlaggingRulePages(driver).click_confirm_deactivate_activate()
        Shared(driver).click_submit()
        driver.get(internal_url.rstrip("/") + "/flags/rules/")


@given("I create all types of flag except organisation")
def add_all_flags(api_test_client, context):
    levels = ["Case", "Good", "Destination"]
    flags = {}
    for level in levels:
        flag = api_test_client.flags.add_flag(level + utils.get_formatted_date_time_y_m_d_h_s(), level)
        flags[level] = {"id": flag["id"], "name": flag["name"]}
    context.flags = flags

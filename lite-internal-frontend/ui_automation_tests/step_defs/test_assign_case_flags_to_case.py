from pytest_bdd import when, then, scenarios, given, parsers

from fixtures.add_a_flag import get_flag_of_level
from pages.application_page import ApplicationPage
from pages.assign_flags_to_case import CaseFlagsPages
from pages.case_page import CasePage
import shared.tools.helpers as utils
from pages.organisation_page import OrganisationPage
from pages.shared import Shared
from shared import functions

scenarios("../features/assign_case_flags_to_case.feature", strict_gherkin=False)


@when("I click edit flags on the first destination")
def click_edit_destination_flags_link(driver):
    case_page = CasePage(driver)
    case_page.select_destination(0)
    case_page.click_edit_destinations_flags()


@when("I click edit flags on the first good")
def click_edit_goods_flags_link(driver):
    case_page = CasePage(driver)
    case_page.select_first_good()
    case_page.click_edit_goods_flags()


@then("the previously created goods flag is assigned to the good")
def assert_flag_is_assigned(driver, context):
    assert CasePage(driver).is_goods_flag_applied(context.flag_name)


@then(parsers.parse('the "{audit_type}" flag appears in the audit trail'))
def verify_organisation_flag_audit(driver, context, audit_type):
    body = Shared(driver).get_audit_trail_text()
    assert context.flags["Organisation"]["name"] in body
    assert audit_type in body


@then("I see added flags to case in case view")
def see_added_flags_to_case(driver, context):
    list_of_flags = driver.execute_script("return document.getElementById('case-flags').textContent")
    for level in context.flags:
        assert context.flags[level]["name"] in list_of_flags


@given("all types of flags exist")
def get_all_flags(api_test_client, context):
    levels = ["Case", "Good", "Organisation", "Destination"]
    flags = {}
    all_flags = api_test_client.flags.get_list_of_flags()
    for level in levels:
        flag = get_flag_of_level(all_flags, level)
        if not flag:
            name = level + utils.get_formatted_date_time_y_m_d_h_s()
            flag = api_test_client.flags.add_flag(name[:25], level)
        flags[level] = {"id": flag["id"], "name": flag["name"]}
    context.flags = flags


@when(parsers.parse('I select a "{level}" flag'))  # noqa
def assign_flags_to_case(driver, context, level):  # noqa
    CaseFlagsPages(driver).select_flag(context.flags[level]["name"])
    functions.click_submit(driver)


@when(parsers.parse('I deselect a "{level}" flag'))  # noqa
def assign_flags_to_case(driver, context, level):  # noqa
    CaseFlagsPages(driver).deselect_flag(context.flags[level]["name"])
    functions.click_submit(driver)


@when("I go to the organisation which submitted the case")  # noqa
def go_to_the_organisation_which_submitted_the_case(driver):  # noqa
    ApplicationPage(driver).go_to_organisation()


@when("I click the edit flags link")  # noqa
def go_to_edit_flags(driver):  # noqa
    OrganisationPage(driver).click_edit_organisation_flags()

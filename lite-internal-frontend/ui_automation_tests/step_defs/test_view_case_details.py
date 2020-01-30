from pytest_bdd import then, scenarios, when, given

from pages.application_page import ApplicationPage
from pages.case_list_page import CaseListPage
from shared.tools.utils import get_lite_client
import shared.tools.helpers as utils

from ui_automation_tests.shared import functions

scenarios("../features/view_case_details.feature", strict_gherkin=False)


def assert_party_data(table, headings, values):
    for heading in headings:
        assert heading.lower() in table.lower()
    for value in values:
        assert value in table


@given("I am an assigned user for the case")
def i_am_an_assigned_user_for_the_case(driver, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_queue.add_queue("User Amendment Queue Testing" + str(utils.get_formatted_date_time_d_h_m_s()))
    lite_client.seed_case.assign_case_to_queue(context.app_id, lite_client.context["queue_id"])
    lite_client.seed_case.assign_case_to_user(context.app_id, lite_client.context["queue_id"], context.gov_user_id)


@when("the exporter user has edited the case")
def exporter_user_has_edited_case(driver, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_case.edit_case(context.app_id)


@when("I click on the exporter amendments banner")
def i_click_on_the_exporter_amendments_banner(driver, context):
    case_list_page = CaseListPage(driver)
    case_list_page.click_on_exporter_amendments_banner()


@then("I can see the case on the exporter amendments queue")
def i_can_see_the_case_on_the_exporter_amendments_queue(driver, context):
    case_list_page = CaseListPage(driver)
    case_list_page.assert_case_is_present(context.app_id)


@then("I see that changes have been made to the case")
def changes_have_been_made_to_case(driver, context, exporter_info, seed_data_config):
    app_page = ApplicationPage(driver)
    case_notification_anchor = app_page.get_case_notification_anchor()

    lite_client = get_lite_client(context, seed_data_config)

    last_exporter_case_activity_id = app_page.get_case_activity_id_by_audit_text(
        context.app_name, lite_client.context["edit_case_app"]["name"]
    )
    expected_anchor_href = driver.current_url + "#" + last_exporter_case_activity_id

    assert case_notification_anchor.get_attribute("href") == expected_anchor_href


@then("I see an end user")
def i_see_end_user_on_page(driver, context):
    destinations_table = ApplicationPage(driver).get_text_of_eu_table()
    headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
    values = [
        # For whatever reason end user subtype is a dict rather than a string
        context.end_user["sub_type"]["value"],
        context.end_user["name"],
        context.end_user["website"],
        context.end_user["address"],
        context.end_user["country"]["name"],
    ]
    assert_party_data(destinations_table, headings, values)


@then("I see an ultimate end user")
def i_see_ultimate_end_user_on_page(driver, context):
    destinations_table = ApplicationPage(driver).get_text_of_ueu_table()
    headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
    values = [
        # context.ultimate_end_user['sub_type'],
        context.ultimate_end_user["name"],
        context.ultimate_end_user["website"],
        context.ultimate_end_user["address"],
        context.ultimate_end_user["country"]["name"],
    ]
    assert_party_data(destinations_table, headings, values)


@then("I see a consignee")
def i_see_consignee_on_page(driver, context):
    destinations_table = ApplicationPage(driver).get_text_of_consignee_table()
    headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
    values = [
        # context.consignee['sub_type'],
        context.consignee["name"],
        context.consignee["website"],
        context.consignee["address"],
        context.consignee["country"]["name"],
    ]
    assert_party_data(destinations_table, headings, values)


@then("I see assigned users")
def i_see_assigned_users_to_the_case_on_page(driver, context):
    assert functions.element_with_id_exists(driver, ApplicationPage(driver).ASSIGNED_USERS_ID)


@then("I see assigned queues")
def i_see_assigned_users_to_the_case_on_page(driver, context):
    assert functions.element_with_id_exists(driver, ApplicationPage(driver).CASE_QUEUES_ID)


@then("I see a third party")
def i_see_third_party_on_page(driver, context):
    destinations_table = ApplicationPage(driver).get_text_of_third_parties_table()
    headings = ["NAME", "TYPE", "WEBSITE", "ADDRESS", "DOCUMENT"]
    values = [
        # context.third_party['sub_type'],
        context.third_party["name"],
        context.third_party["website"],
        context.third_party["address"],
        context.third_party["country"]["name"],
    ]
    assert_party_data(destinations_table, headings, values)

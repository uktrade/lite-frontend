from pytest_bdd import then, scenarios, when, given

import shared.tools.helpers as utils
from pages.application_page import ApplicationPage
from pages.case_list_page import CaseListPage
from pages.case_page import CasePage

scenarios("../features/view_standard_application.feature", strict_gherkin=False)


@given("I am an assigned user for the case")
def i_am_an_assigned_user_for_the_case(context, api_test_client):
    api_test_client.queues.add_queue("User Amendment Queue Testing" + str(utils.get_formatted_date_time_d_h_m_s()))
    api_test_client.cases.assign_case_to_queue(context.app_id, api_test_client.context["queue_id"])
    api_test_client.cases.assign_case_to_user(context.app_id, api_test_client.context["queue_id"], context.gov_user_id)


@given("the exporter user has edited the case")
def exporter_user_has_edited_case(context, api_test_client):
    api_test_client.cases.edit_case(context.app_id)


@given("the exporter has deleted the third party")
def exporter_has_deleted_end_user(context, api_test_client):
    api_test_client.applications.parties.delete_party(draft_id=context.app_id, party=context.third_party)


@when("I click on the exporter amendments banner")
def i_click_on_the_exporter_amendments_banner(driver, context):
    case_list_page = CaseListPage(driver)
    case_list_page.click_on_exporter_amendments_banner()


@then("I can see the case on the exporter amendments queue")
def i_can_see_the_case_on_the_exporter_amendments_queue(driver, context):
    case_list_page = CaseListPage(driver)
    case_list_page.assert_case_is_present(context.app_id)


@then("I see that changes have been made to the case")
def changes_have_been_made_to_case(driver, context, api_test_client):
    assert len(ApplicationPage(driver).get_case_notification_anchor())


@then("I see the application destinations")
def i_see_destinations(driver, context):
    destinations = [context.consignee, context.end_user, context.third_party, context.ultimate_end_user]
    destinations_table_text = CasePage(driver).get_destinations_text()

    for destination in destinations:
        assert destination["name"] in destinations_table_text


@then("I see an inactive party on page")
def i_see_inactive_party(driver, context):
    destinations = [context.third_party]
    destinations_table_text = CasePage(driver).get_deleted_entities_text()

    for destination in destinations:
        assert destination["name"] in destinations_table_text

from datetime import date

from selenium.webdriver.common.by import By

import tests_common.tools.helpers as utils
from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.case_list_page import CaseListPage
from ui_tests.caseworker.pages.case_page import CasePage
from pytest_bdd import then, scenarios, when, given, parsers

scenarios("../features/view_standard_application.feature", strict_gherkin=False)


@given("I am an assigned user for the case")
def i_am_an_assigned_user_for_the_case(context, api_test_client):
    api_test_client.queues.add_queue(f"User Amendment Queue Testing {utils.get_formatted_date_time_d_h_m_s()}")
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


@then("I should see the view link displayed against a good")  # noqa
def i_see_good_details_view_link(driver, context):  # noqa
    goods = CasePage(driver).get_goods()
    for good in goods:
        view_link_table_cell = good.find_element_by_css_selector("td#view-good-details")
        if view_link_table_cell:
            assert "View" in view_link_table_cell.text


@then("I see an inactive party on page")
def i_see_inactive_party(driver, context):
    destinations = [context.third_party]
    destinations_table_text = CasePage(driver).get_deleted_entities_text()

    for destination in destinations:
        assert destination["name"] in destinations_table_text


@then(parsers.parse('the "{party_type}" name is "{name}", address is "{address}", country is "{country}"'))
def filter_by_application_type(driver, party_type, name, address, country):
    destinations = driver.find_element_by_id("table-destinations")
    party_index = {"End user": 1, "Consignee": 2}
    index = party_index.get(party_type, 1)
    party = destinations.find_element_by_xpath(f".//tbody/tr[{index}]")
    party_type_text = party.find_element_by_xpath(".//th").text
    party_name = party.find_element_by_xpath(".//td[2]").text
    party_address = party.find_element_by_xpath(".//td[3]").text

    assert party_type_text == party_type
    assert party_name == name
    assert party_address == f"{address}, {country}"


@then(parsers.parse('the intended end use details should be "{end_use_expected}"'))
def filter_by_application_type(driver, end_use_expected):
    end_use_table = driver.find_element_by_id("slice-end-use-details")
    end_use_text = end_use_table.find_element_by_xpath(".//tbody/tr[1]/td[3]").text
    assert end_use_text == end_use_expected


@then("I should see a link to download the document")
def i_see_link_to_download_document(driver):
    docs = driver.find_elements(by=By.CLASS_NAME, value="app-documents__item")
    assert len(docs) == 1
    link = docs[0].find_element_by_class_name("app-documents__item-details")
    assert link.text.startswith(f"Application Form - {date.today().isoformat()}")

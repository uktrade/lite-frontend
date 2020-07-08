from datetime import datetime

from pytest_bdd import given, when, then, scenarios

from ui_automation_tests.pages.attach_document_page import AttachDocumentPage
from ui_automation_tests.pages.compliance_pages import CompliancePages
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.pages.open_licence_returns_page import OpenLicenceReturnsPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.tools.utils import create_temporary_file, get_temporary_file_path

scenarios("../features/compliance.feature", strict_gherkin=False)


@given("I produce an open licence CSV with for my licence")
def create_open_licence_return(context):
    context.open_licence_csv_filename = "open_licence_returns.csv"
    text = f"\n{context.reference_code},a,b,c,d"
    create_temporary_file(context.open_licence_csv_filename, text)


@given("I create a visit case for the linked compliance case")
def create_visit_case(context, decision, api_test_client):
    context.comp_site_case_id = api_test_client.cases.get_compliance_id_for_case(context.case_id)[0]
    context.visit_case_id = api_test_client.cases.create_compliance_visit_case(context.comp_site_case_id)


@when("I complete an open licence return")
def go_to_add_open_licence_return(driver, context):
    # Go to form
    open_licence_returns_page = OpenLicenceReturnsPage(driver)
    ExporterHubPage(driver).click_open_licence_returns()
    open_licence_returns_page.click_submit_return()

    # Fill out details (skip info page)
    context.open_licence_return_year = str(datetime.now().year)
    functions.click_submit(driver)
    open_licence_returns_page.select_year(context.open_licence_return_year)
    functions.click_submit(driver)
    file_path = get_temporary_file_path(context.open_licence_csv_filename)
    AttachDocumentPage(driver).choose_file(file_path)
    functions.click_submit(driver)


@then("I see the success page")
def success_page(driver, context):
    context.open_licence_returns_id = driver.current_url.split("/open-licence-returns/")[1].split("/success/")[0]
    assert OpenLicenceReturnsPage(driver).success_panel_is_present()


@when("I go to my open licence returns")
def go_to_open_licence_returns(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/compliance/open-licence-returns/")


@then("I see my open licence return is the latest entry")
def see_open_licence_entry(driver, context):
    top_row = Shared(driver).get_table_row(1)
    assert top_row.get_attribute("id") == context.open_licence_returns_id
    assert context.open_licence_return_year in top_row.text


@when("I view my organisations compliance section")
def view_compliance_tile(driver):
    ExporterHubPage(driver).click_compliance()


@then("I can see the compliance case in the list of cases")
def case_in_compliance_list(driver, context):
    assert CompliancePages(driver).find_paginated_compliance_site_case_row(context.comp_site_case_id)


@when("I view the compliance case")
def view_compliance_case(driver, context):
    CompliancePages(driver).view_compliance_case(context.comp_site_case_id)


@then("I can see the contents of the compliance case")
def all_tabs_are_visible(driver):
    page = CompliancePages(driver)
    assert page.details_tab()
    assert page.ecju_queries_tab()
    assert page.notes_tab()
    assert page.generated_documents_tab()
    assert page.visits_tab()


@then("I can see one visit case is created")
def visit_case_created(driver, context):
    page = CompliancePages(driver)
    page.visits_tab().click()
    assert page.find_paginated_compliance_visit_case(context.visit_case_id)


@then("I view the visit case where I can see a smaller set of tabs are visible")
def view_visit_case_and_check_tabs(driver, context):
    page = CompliancePages(driver)
    page.view_visit_case(context.visit_case_id)
    assert page.ecju_queries_tab()
    assert page.generated_documents_tab()

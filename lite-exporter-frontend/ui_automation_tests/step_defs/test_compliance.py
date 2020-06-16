from datetime import datetime

from pytest_bdd import given, when, then, scenarios

from ui_automation_tests.pages.attach_document_page import AttachDocumentPage
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

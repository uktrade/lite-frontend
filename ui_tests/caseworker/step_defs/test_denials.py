import uuid

from pytest_bdd import given, then, scenarios, parsers, when

from ui_tests.caseworker.pages.add_denial_records_page import AddDenialRecordsPage
from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.denial_records_page import DenialRecordsPage
from ui_tests.caseworker.pages.shared import Shared


scenarios("../features/denials.feature", strict_gherkin=False)


@when("I go to the add denial records page")
def go_to_add_denial_records_page(driver, internal_url):
    driver.get(f'{internal_url.rstrip("/")}/denials/upload/')


@when("I download an example .csv file")
def download_example_csv_file(driver):
    AddDenialRecordsPage(driver).download_example_csv_file()


@when(
    "I update the .csv file with <name>,<address>,<notifying_govmt>,<final_dest>,<item_list_codes>,<item_desc>,<consignee_name>,<end_use>"
)
def update_example_csv_file(
    driver, name, address, notifying_govmt, final_dest, item_list_codes, item_desc, consignee_name, end_use
):

    AddDenialRecordsPage(driver).update_example_csv_file(
        reference=str(uuid.uuid4()),
        name=name,
        address=address,
        notifying_government=notifying_govmt,
        final_destination=final_dest,
        item_list_codes=item_list_codes,
        item_description=item_desc,
        consignee_name=consignee_name,
        end_use=end_use,
    )


@when("I upload the .csv file")
def upload_csv_file(driver):
    AddDenialRecordsPage(driver).upload_csv_file()


@then(parsers.parse('I should see a banner that says "{banner_text}"'))
def should_see_banner_text(driver, banner_text):
    assert banner_text in AddDenialRecordsPage(driver).get_banner_text()


@when(parsers.parse('I select end user "{end_user}"'))
def select_end_user(driver, end_user):
    ApplicationPage(driver).select_end_user(end_user)


@then(parsers.parse('I should see "{name}" listed'))
def should_see_name_listed(driver, name):
    DenialRecordsPage(driver).get_row_for_name(name)


@when(parsers.parse('I select "{name}"'))
def select_name(driver, name):
    DenialRecordsPage(driver).select_row_for_name(name)


@then(parsers.parse('I should see "{name}" as a partial match'))
def should_see_partial_match(driver, name):
    assert name in ApplicationPage(driver).get_matches("PARTIAL MATCH")


@then(parsers.parse('I should not see "{name}" as a partial match'))
def should_not_see_partial_match(driver, name):
    assert "PARTIAL MATCH" not in Shared(driver).get_text_of_body()


@then(parsers.parse('I should see "{name}" as an exact match'))
def should_see_exact_match(driver, name):
    assert name in ApplicationPage(driver).get_matches("EXACT MATCH")


@then(parsers.parse('I should not see "{name}" as an exact match'))
def should_not_see_exact_match(driver, name):
    assert "EXACT MATCH" not in Shared(driver).get_text_of_body()


@when(parsers.parse('I select "{name}" under denial matches'))
def select_denial_match(driver, name):
    ApplicationPage(driver).select_denial_match(name)


@given("I cleanup any temporary files created")
def cleanup_temporary_files(driver):
    AddDenialRecordsPage(driver).cleanup_temporary_files()

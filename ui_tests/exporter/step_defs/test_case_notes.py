from pytest_bdd import given, when, then, scenarios, parsers

import tests_common.tools.helpers as utils
from ui_tests.exporter.pages.submitted_applications_page import SubmittedApplicationsPages
from ui_tests.exporter.pages.application_page import ApplicationPage

scenarios("../features/case_notes.feature", strict_gherkin=False)


@then("note is displayed")
def note_is_displayed(driver, context):
    application_page = SubmittedApplicationsPages(driver)
    assert context.text in application_page.get_text_of_case_note(0)
    assert utils.search_for_correct_date_regex_in_element(
        application_page.get_text_of_case_note_date_time(0)
    ), "incorrect time of post on case note"


@when("I click cancel button")
def i_click_cancel_button(driver):
    application_page = SubmittedApplicationsPages(driver)
    application_page.click_cancel_button()


@then("entered text is no longer in case note field")
def entered_text_no_longer_in_case_field(driver, context):
    application_page = SubmittedApplicationsPages(driver)
    assert context.text not in application_page.get_text_of_case_note_field()


@given(parsers.parse('caseworker inputs a case note as "{case_note}"'))
def caseworker_create_case_note(driver, case_note, api_test_client, context):
    api_test_client.cases.add_case_note(context, context.case_id, note=case_note)


@then("I see a notification next to Notes")
def should_see_notification_ecju_queries(driver):
    assert ApplicationPage(driver).notes_notification_count() == "1"


@then(parsers.parse('I see "{case_note}" as the case notes'))
def i_see_case_notes(driver, case_note):
    assert ApplicationPage(driver).get_text_of_case_note(0) == case_note

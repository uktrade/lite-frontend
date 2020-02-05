from pytest_bdd import when, then, scenarios

import shared.tools.helpers as utils
from pages.submitted_applications_page import SubmittedApplicationsPages

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
    application_page.click_cancel_btn()


@then("entered text is no longer in case note field")
def entered_text_no_longer_in_case_field(driver):
    application_page = SubmittedApplicationsPages(driver)
    assert "Case note to cancel" not in application_page.get_text_of_case_note_field()

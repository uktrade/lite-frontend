from pytest_bdd import when, then, parsers, scenarios, given

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


@then(parsers.parse('case note warning is "{text}"'))
def n_characters_remaining(driver, text):
    application_page = SubmittedApplicationsPages(driver)
    assert application_page.get_text_of_case_note_warning() == text


@then("post note is disabled")
def post_note_is_disabled(driver):
    application_page = SubmittedApplicationsPages(driver)
    assert application_page.get_disabled_attribute_of_post_note() == "true"


@then("entered text is no longer in case note field")
def entered_text_no_longer_in_case_field(driver):
    application_page = SubmittedApplicationsPages(driver)
    assert "Case note to cancel" not in application_page.get_text_of_case_note_field()


@then("the case note text area is not present")
def edit_button_not_present(driver):
    driver.set_timeout_to(0)
    assert len((SubmittedApplicationsPages(driver).find_case_note_text_area())) == 0
    driver.set_timeout_to(10)

import time
from pytest_bdd import when, then, parsers, scenarios
from ui_tests.caseworker.pages.application_page import ApplicationPage
import tests_common.tools.helpers as utils
from tests_common import functions

scenarios("../features/case_notes.feature", strict_gherkin=False)


@when(parsers.parse('I enter "{text}" as the case note'))
def enter_case_note_text(driver, text, context):
    application_page = ApplicationPage(driver)
    if text == "too many characters":
        text = "T" * 2201
    context.text = text
    application_page.enter_case_note(text)


@when("I click post note")
def click_post_note(driver, context):
    application_page = ApplicationPage(driver)
    application_page.click_post_note_btn()
    context.date_time_of_post = utils.get_formatted_date_time_h_m_pm_d_m_y()


@when("I click cancel button")
def i_click_cancel_button(driver):
    application_page = ApplicationPage(driver)
    application_page.click_cancel_btn()


@then("the case note is disabled")
def post_note_is_disabled(driver):
    assert functions.element_with_css_selector_exists(driver, ".lite-case-note__container--error")


@then("entered text is no longer in case note field")
def entered_text_no_longer_in_case_field(driver, context):
    application_page = ApplicationPage(driver)
    assert context.text not in application_page.get_text_of_case_note_field(), "cancel button hasn't cleared text"


@when("I click make visible to exporter")
def click_visible_to_exporters_checkbox(driver):
    application_page = ApplicationPage(driver)
    application_page.click_visible_to_exporter_checkbox()


@when("I click confirm on confirmation box")
def click_confirm_on_confirmation_box(driver):
    alert = driver.switch_to.alert
    alert.accept()

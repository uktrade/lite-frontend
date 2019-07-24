from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.application_page import ApplicationPage
import helpers.helpers as utils

scenarios('../features/case_notes.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when(parsers.parse('I enter "{text}" for case note'))
def enter_case_note_text(driver, text, context):
    application_page = ApplicationPage(driver)
    if text == 'the maximum limit with spaces':
        text = utils.repeat_to_length(" ", 2200)
    elif text == 'the maximum limit':
        text = utils.repeat_to_length("T", 2200)
    context.text = text
    application_page.enter_case_note(text)


@when('I click post note')
def click_post_note(driver, context):
    application_page = ApplicationPage(driver)
    application_page.click_post_note_btn()
    context.date_time_of_post = utils.get_formatted_date_time_h_m_pm_d_m_y()


@then('note is displayed')
def note_is_displayed(driver, context):
    application_page = ApplicationPage(driver)
    assert context.text in application_page.get_text_of_case_note(0)
    assert context.date_time_of_post.split(":")[1] in application_page.get_text_of_case_note_date_time(0).split(":")[1], "incorrect time of post on case note"


@when('I click cancel button')
def i_click_cancel_button(driver):
    application_page = ApplicationPage(driver)
    application_page.click_cancel_btn()


@then('maximum case error is displayed')
def maximum_error_message_is_displayed(driver):
    error_message = driver.find_element_by_css_selector("h1").text
    error_body = driver.find_elements_by_css_selector(".govuk-body")
    assert error_message == "An error occurred", "should not be able to post an empty case note with space characters"
    assert error_body[0].text == "Case note may not be blank.", "should not be able to post an empty case note with space characters"
    assert error_body[1].text == "You can go back by clicking the back button at the top of the page.", "should not be able to post an empty case note with space characters"


@then(parsers.parse('case note warning is "{text}"'))
def n_characters_remaining(driver, text):
    if text == "disabled":
        assert "disabled" in driver.find_element_by_id("button-post-note").get_attribute("class"), "post note button is not disabled"
    else:
        assert "disabled" not in driver.find_element_by_id("button-post-note").get_attribute("class"), "post note button is disabled"


@then('post note is disabled')
def post_note_is_disabled(driver):
    application_page = ApplicationPage(driver)
    assert application_page.get_disabled_attribute_of_post_note() == "true"


@then('entered text is no longer in case note field')
def entered_text_no_longer_in_case_field(driver):
    application_page = ApplicationPage(driver)
    assert "Case note to cancel" not in application_page.get_text_of_case_note_field()


@when('I click visible to exporters checkbox')
def click_visible_to_exporters_checkbox(driver):
    application_page = ApplicationPage(driver)
    application_page.click_visible_to_exporter_checkbox()


@when("I click confirm on confirmation box")
def click_confirm_on_confirmation_box(driver):
    alert = driver.switch_to_alert()
    alert.accept()

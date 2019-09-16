from pytest_bdd import when, then, parsers, scenarios, given

from pages.shared import Shared
from pages.submitted_applications_page import SubmittedApplicationsPages

import helpers.helpers as utils

scenarios('../features/case_notes.feature', strict_gherkin=False)


@given('an application exists')
def application_exists_case_note_added(add_an_application):
    pass


@when('I click on application previously created')
def click_on_an_application(driver, context):
    driver.find_element_by_partial_link_text(context.app_name).click()


@when(parsers.parse('I enter "{text}" for case note'))
def enter_case_note_text(driver, text, context):
    application_page = SubmittedApplicationsPages(driver)
    if text == 'the maximum limit with spaces':
        text = ' ' * 2200
    elif text == 'the maximum limit':
        text = 'T' * 2200
    elif text == 'the maximum limit plus 1':
        text = 'T' * 2201
    context.text = text
    application_page.enter_case_note(text)


@when('I click post note')
def click_post_note(driver, context):
    application_page = SubmittedApplicationsPages(driver)
    application_page.click_post_note_btn()
    context.date_time_of_post = utils.get_formatted_date_time_h_m_pm_d_m_y()


@then('note is displayed')
def note_is_displayed(driver, context):
    application_page = SubmittedApplicationsPages(driver)
    assert context.text in application_page.get_text_of_case_note(0)
    assert utils.split_and_replace_date_time(context.date_time_of_post) in utils.split_and_replace_date_time(application_page.get_text_of_case_note_date_time(0)), 'incorrect time of post on case note'


@when('I click cancel button')
def i_click_cancel_button(driver):
    application_page = SubmittedApplicationsPages(driver)
    application_page.click_cancel_btn()


@then(parsers.parse('case note warning is "{text}"'))
def n_characters_remaining(driver, text):
    application_page = SubmittedApplicationsPages(driver)
    assert application_page.get_text_of_case_note_warning() == text


@then('post note is disabled')
def post_note_is_disabled(driver):
    application_page = SubmittedApplicationsPages(driver)
    assert application_page.get_disabled_attribute_of_post_note() == 'true'


@then('entered text is no longer in case note field')
def entered_text_no_longer_in_case_field(driver):
    application_page = SubmittedApplicationsPages(driver)
    assert 'Case note to cancel' not in application_page.get_text_of_case_note_field()

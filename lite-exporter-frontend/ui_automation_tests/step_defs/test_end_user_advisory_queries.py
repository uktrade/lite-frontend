from pytest_bdd import when, then, parsers, scenarios, given

import shared.tools.helpers as utils
from pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from pages.end_user_advisory_page import EndUserAdvisoryPage
from pages.respond_to_ecju_query_page import RespondToEcjuQueryPage
from pages.shared import Shared
from shared import functions
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.submitted_applications_page import SubmittedApplicationsPages

scenarios("../features/end_user_advisory_queries.feature", strict_gherkin=False)


@given("An end user advisory with a case note has been added via gov user")
def end_user_advisory_exists_case_note_added(
    driver, add_end_user_advisory, internal_case_note_end_user_advisory, context
):
    pass


@given("An end user advisory with an ecju query has been added via gov user")
def end_user_advisory_exists_ecju_query_added(
    driver, add_end_user_advisory, internal_ecju_query_end_user_advisory, context
):
    pass


@when("I select to create a new advisory")
def apply_for_end_user_advisory(driver):
    end_user_advisory_page = EndUserAdvisoryPage(driver)
    end_user_advisory_page.click_apply_for_advisories()
    functions.click_submit(driver)


@when(parsers.parse('I select "{type}" user type and continue'))
def select_end_user_type(driver, type):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.select_type(type, prefix)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{name}" for the name'))
def add_user_details(driver, name):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_name(name, prefix)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{nature}" for the nature of business'))
def add_user_details(driver, nature):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_nature(nature)
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter "{name}" for the primary contact name, "{job}" for primary contact_job_title, "{email}" for the primary contact email, "{telephone}" for the primary contact telephone'
    )
)
def add_user_details(driver, name, email, telephone, job):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_primary_contact_email(email)
    end_user_page.enter_primary_contact_name(name)
    end_user_page.enter_primary_contact_job_title(job)
    end_user_page.enter_primary_contact_telephone(telephone)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{address}" for the address, "{country}" as the country and continue'))
def add_user_details(driver, address, country):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_address(address, prefix)
    end_user_page.enter_country(country, prefix)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{reasoning}" for my reason, and "{notes}" for notes and click submit'))
def enter_advisory_details(driver, reasoning, notes):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_reasoning(reasoning)
    end_user_page.enter_notes(notes)
    functions.click_submit(driver)


@when("I click copy on an existing end user advisory")
def click_copy(driver):
    no = utils.get_element_index_by_text(Shared(driver).get_table_rows(), "Commercial", complete_match=False)
    Shared(driver).get_table_row(no).find_element_by_link_text("Copy").click()


@when(parsers.parse('I enter "{name}" for the name and continue'))
def enter_name(driver, name):
    prefix = "end_user."
    AddEndUserAdvisoryPages(driver).enter_name(name, prefix)
    functions.click_submit(driver)


@when("I open an end user advisory already created")
def open_already_created_end_user_advisory(driver, context):
    EndUserAdvisoryPage(driver).open_advisory_by_reference_code(context.end_user_advisory_id)


@then("I see a notification on end user advisory list")
def notification_on_end_user_advisory_list(driver, context):
    # Commenting out due to bug LT-1433
    # assert EndUserAdvisoryPage(driver).confirm_advisory_displayed_by_reference_code(context.end_user_advisory_id)
    pass


@then("I see a notification for case note and can view the case note")
def notification_on_notes_tab(driver, context):
    enduseradvisorypage = EndUserAdvisoryPage(driver)
    # Commenting out due to bug LT-1433
    # assert '1' in enduseradvisorypage.case_note_notification_bubble_text()
    assert context.case_note_text in enduseradvisorypage.latest_case_note_text()


@then(parsers.parse('I can view "{text}" in case notes'))
def notification_on_notes_tab(driver, text):
    assert text in EndUserAdvisoryPage(driver).latest_case_note_text()


@when(parsers.parse('I enter "{text}" for case note'))
def enter_case_note_text(driver, text):
    application_page = SubmittedApplicationsPages(driver)
    application_page.enter_case_note(text)
    application_page.click_post_note_btn()


@when("I click to respond to the ecju query")
def click_to_respond_to_ecju_query(driver):
    application_page = ApplicationPage(driver)
    application_page.respond_to_ecju_query(0)


@when(parsers.parse('I enter "{response}" for ecju query and click submit'))
def respond_to_query(driver, response):
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)
    functions.click_submit(driver)


@when(parsers.parse('I select "{value}" for submitting response and click submit'))
def submit_response_confirmation(driver, value):
    driver.find_element_by_id("confirm_response-" + value).click()
    driver.find_element_by_css_selector(".govuk-button").click()


@then("I see my ecju query is closed")
def determine_that_there_is_a_closed_query(driver):
    application_page = ApplicationPage(driver)
    closed_queries = application_page.get_count_of_closed_ecju_queries()
    assert closed_queries > 0

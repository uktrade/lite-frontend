from pytest_bdd import when, then, parsers, scenarios, given

import shared.tools.helpers as utils
from pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from pages.end_user_advisory_page import EndUserAdvisoryPage
from pages.shared import Shared
from shared import functions
from shared.tools.utils import get_lite_client

scenarios("../features/end_user_advisory_queries.feature", strict_gherkin=False)


@given("An end user advisory with a case note has been added via gov user")
def end_user_advisory_exists_case_note_added(add_end_user_advisory, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_case.add_case_note(context, context.end_user_advisory_id)


@given("An end user advisory with an ecju query has been added via gov user")
def end_user_advisory_exists_ecju_query_added(add_end_user_advisory, context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_ecju.add_ecju_query(context.end_user_advisory_id)


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
    EndUserAdvisoryPage(driver).open_end_user_advisory(context.end_user_advisory_id)


@then("I see a notification on end user advisory list")
def notification_on_end_user_advisory_list(driver, context):
    assert EndUserAdvisoryPage(driver).is_end_user_advisory_displayed_with_notification(context.end_user_advisory_id)


@then("I see a notification for case note and can view the case note")
def notification_on_notes_tab(driver, context):
    end_user_advisory_page = EndUserAdvisoryPage(driver)
    assert "1" in end_user_advisory_page.case_note_notification_bubble_text()
    assert context.case_note_text in end_user_advisory_page.latest_case_note_text()


@then(parsers.parse('I can view "{text}" in case notes'))
def notification_on_notes_tab(driver, text):
    assert text in EndUserAdvisoryPage(driver).latest_case_note_text()

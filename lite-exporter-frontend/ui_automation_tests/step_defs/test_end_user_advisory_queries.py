from pytest_bdd import when, then, parsers, scenarios, given

import ui_automation_tests.shared.tools.helpers as utils
from ui_automation_tests.pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from ui_automation_tests.pages.end_user_advisory_page import EndUserAdvisoryPage
from ui_automation_tests.shared import functions

scenarios("../features/end_user_advisory_queries.feature", strict_gherkin=False)


@given("An end user advisory with a case note and ecju query has been added via gov user")
def end_user_advisory_exists_case_note_added(add_end_user_advisory, context, api_test_client):
    api_test_client.cases.add_case_note(context, context.end_user_advisory_id)
    api_test_client.ecju_queries.add_ecju_query(context.end_user_advisory_id)


@when("I select to create a new advisory")
def apply_for_end_user_advisory(driver):
    EndUserAdvisoryPage(driver).click_apply_for_advisories()
    functions.click_submit(driver)


@when(parsers.parse('I select "{type}" user type and continue'))
def select_end_user_type(driver, type):
    prefix = "end_user."
    AddEndUserAdvisoryPages(driver).select_type(type, prefix)
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter "{nature}" for the nature of business, "{name}" for the primary contact name, "{job}" for primary contact_job_title, "{email}" for the primary contact email, "{telephone}" for the primary contact telephone, "{address}" for the address, "{country}" as the country and continue'
    )
)
def add_user_details(driver, context, nature, name, job, email, telephone, address, country):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    context.end_user_advisory_name = "EUA-" + utils.get_formatted_date_time_y_m_d_h_s()
    end_user_page.enter_name(context.end_user_advisory_name, prefix)
    end_user_page.enter_nature(nature)
    end_user_page.enter_primary_contact_email(email)
    end_user_page.enter_primary_contact_name(name)
    end_user_page.enter_primary_contact_job_title(job)
    end_user_page.enter_primary_contact_telephone(telephone)
    end_user_page.enter_address(address, prefix)
    end_user_page.enter_country(country, prefix)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{reasoning}" for my reason, and "{notes}" for notes and click submit'))
def enter_advisory_details(driver, reasoning, notes):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_reasoning(reasoning)
    end_user_page.enter_notes(notes)
    functions.click_submit(driver)


@then("I see the success page")
def success_page(driver, context):
    end_user_page = AddEndUserAdvisoryPages(driver)
    assert end_user_page.success_panel_is_present()
    context.end_user_advisory_ecju_reference = end_user_page.get_ecju_reference_from_success_banner()


@when("I go to end user advisories")
def go_to_end_user_advisories(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/end-users/")


@when("I filter by my end user name")
def filter_end_user(driver, context):
    EndUserAdvisoryPage(driver).filter_by_name(context.end_user_advisory_name)


@then("I see my end user advisory")
def see_end_user_advisory(driver, context):
    assert context.end_user_advisory_ecju_reference in EndUserAdvisoryPage(driver).get_row_text()


@when("I click copy on an existing end user advisory")
def click_copy(driver):
    EndUserAdvisoryPage(driver).click_row_copy()


@when(parsers.parse('I enter "{name}" for the name and continue'))
def enter_name(driver, name):
    prefix = "end_user."
    AddEndUserAdvisoryPages(driver).enter_name(name, prefix)
    functions.click_submit(driver)


@when("I open an end user advisory already created")
def open_already_created_end_user_advisory(driver, context):
    EndUserAdvisoryPage(driver).open_end_user_advisory(context.end_user_advisory_id)


@then(parsers.parse('I see my end user advisory with "{total}" notifications'))
def notification_on_end_user_advisory_list(driver, context, total):
    assert total == EndUserAdvisoryPage(driver).row_notifications()


@then("I see a notification for case note and can view the case note")
def notification_on_notes_tab(driver, context):
    end_user_advisory_page = EndUserAdvisoryPage(driver)
    assert "1" in end_user_advisory_page.case_note_notification_bubble_text()
    assert context.case_note_text in end_user_advisory_page.latest_case_note_text()


@then(parsers.parse("I can see my text in the latest case note"))
def notification_on_notes_tab(driver, context):
    assert context.text in EndUserAdvisoryPage(driver).latest_case_note_text()

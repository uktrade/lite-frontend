from pytest_bdd import scenarios, when, parsers, then

from pages.application_page import ApplicationPage
from pages.case_page import CasePage, CaseTabs

scenarios("../features/view_open_application.feature", strict_gherkin=False)


@when("I go to the activity tab")
def go_to_activity_tab(driver, internal_url, context):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)


@when(parsers.parse('filter user_type has been changed to "{user_type}"'))  # noqa
def filter_status_change(driver, user_type):  # noqa
    page = ApplicationPage(driver)
    page.select_filter_user_type_from_dropdown(user_type)


@then("exporter is at the first audit in the trail")  # noqa
def exporter_first_audit_in_trail(driver, exporter_info):  # noqa
    first_audit = CasePage(driver).get_audit_trail_text()
    assert f"{exporter_info['first_name']}" in first_audit
    assert f"{exporter_info['last_name']}" in first_audit


@then("exporter is not in the audit trail")  # noqa
def exporter_is_not_in_audit_trail(driver, exporter_info):  # noqa
    audit = CasePage(driver).get_audit_trail_text()
    assert f"{exporter_info['first_name']}" not in audit
    assert f"{exporter_info['last_name']}" not in audit

from pytest_bdd import scenarios, then

from pages.application_page import ApplicationPage
from pages.shared import Shared

scenarios("../features/manage_cases.feature", strict_gherkin=False)


@then("the status has been changed in the application")  # noqa
def audit_trail_updated(driver, context, internal_info, internal_url):  # noqa
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)

    assert (
        context.status.lower() in Shared(driver).get_audit_trail_text().lower()
    ), "status has not been shown as approved in audit trail"

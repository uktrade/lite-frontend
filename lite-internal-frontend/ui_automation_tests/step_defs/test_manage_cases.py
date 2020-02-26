from pytest_bdd import then, scenarios
from pages.application_page import ApplicationPage

scenarios("../features/manage_cases.feature", strict_gherkin=False)


@then("the application headers and information are correct")
def application_headers_and_info_are_correct(driver, api_url, context):
    application_page = ApplicationPage(driver)
    application_summary = application_page.get_text_of_application_summary_board().lower()
    assert "activity" in application_summary
    assert "submitted at" in application_summary
    assert "trading" in application_summary or "brokering" in application_summary

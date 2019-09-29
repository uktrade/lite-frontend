from pytest_bdd import when, then, parsers, scenarios
from pages.application_page import ApplicationPage
from pages.record_decision_page import RecordDecision

import helpers.helpers as utils


class ManageCases:
    scenarios('../features/manage_cases.feature', strict_gherkin=False)

    import logging
    log = logging.getLogger()
    console = logging.StreamHandler()
    log.addHandler(console)

    @when('I click record decision')
    def click_post_note(driver, context):
        ApplicationPage(driver).click_record_decision()
        context.decision_array = []

    @when(parsers.parse('I select decision "{number}"'))
    def select_decision(driver, number, context):
        record = RecordDecision(driver)
        record.click_on_decision_number(number)
        context.decision_array.append(number)
        context.advice_data.append(number)

    @then('the status has been changed in the application')
    def status_has_been_changed_in_header(driver, context, sso_users_name):
        application_page = ApplicationPage(driver)
        if context.status.lower() == "under review":
            assert "updated the status to " + "under_review" in application_page.get_text_of_audit_trail_item(
                0), "status has not been shown as approved in audit trail"
        else:
            assert "updated the status to " + context.status.lower() in application_page.get_text_of_audit_trail_item(0), "status has not been shown as approved in audit trail"

        assert utils.search_for_correct_date_regex_in_element(application_page.get_text_of_activity_dates(0)), "date is not displayed after status change"
        assert application_page.get_text_of_activity_users(0) == sso_users_name, "user who has made the status change has not been displayed correctly"

    @then('the application headers and information are correct')
    def application_headers_and_info_are_correct(driver, api_url, context):
        application_page = ApplicationPage(driver)
        application_summary = application_page.get_text_of_application_summary_board()
        assert "APPLICANT" in application_summary
        assert "ACTIVITY" in application_summary
        assert "CREATED AT" in application_summary
        assert "REFERENCE NUMBER" in application_summary
        assert "LICENCE TYPE" in application_summary
        assert context.org_name in application_summary
        assert "Trading" in application_summary or "Brokering" in application_summary
        assert utils.search_for_correct_date_regex_in_element(application_summary)
        assert "None" in application_summary
        assert "Standard Licence" in application_summary

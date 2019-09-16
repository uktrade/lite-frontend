from pytest_bdd import when, then, parsers, scenarios
from pages.application_page import ApplicationPage
from pages.record_decision_page import RecordDecision
from pages.shared import Shared
import helpers.helpers as utils

from ui_automation_tests.pages.roles_pages import RolesPages

from pages.header_page import HeaderPage
from ui_automation_tests.pages.users_page import UsersPage


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

    @when(parsers.parse('I "{grant_or_deny}" application'))
    def grant_or_deny_decision(driver, grant_or_deny, context):
        record = RecordDecision(driver)
        if grant_or_deny == "grant":
            record.click_on_grant_licence()
        elif grant_or_deny == "deny":
            record.click_on_deny_licence()
            context.advice_data = []

    @when(parsers.parse('I type optional text "{optional_text}"'))
    def type_optional_text(driver, optional_text, context):
        record = RecordDecision(driver)
        record.enter_optional_text(optional_text)
        context.optional_text = optional_text

    @when(parsers.parse('I select decision "{number}"'))
    def select_decision(driver, number, context):
        record = RecordDecision(driver)
        record.click_on_decision_number(number)
        context.decision_array.append(number)
        context.advice_data.append(number)

    @then('I see denied reason')
    def denied_reason(driver, context):
        body = Shared(driver).get_text_of_body()
        assert "Further information" in body
        assert context.optional_text in body

    @then(parsers.parse('I see application "{grant_or_deny}"'))
    def see_application_granted_or_denied(driver, grant_or_deny, context):
        application_page = ApplicationPage(driver)
        if grant_or_deny == "granted":
            assert "updated the status to approved" in application_page.get_text_of_audit_trail_item(0), "status has not been shown as approved in audit trail"
        elif grant_or_deny == "denied":
            assert "updated the status to under_final_review" in application_page.get_text_of_audit_trail_item(0), "status has not been shown as under review in audit trail"
            body = Shared(driver).get_text_of_body()
            assert "This case was denied because" in body
            for denial_reason_code in context.decision_array:
                assert denial_reason_code in body



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
        assert "LAST UPDATED" in application_summary
        assert context.org_name in application_summary
        assert "Trading" in application_summary or "Brokering" in application_summary
        assert context.date_time_of_update.split(':')[1] in application_summary
        assert "None" in application_summary
        assert "Standard Licence" in application_summary

    @when(parsers.parse('I give myself the required permissions for "{permission}"'))
    def get_required_permissions(driver, permission):
        roles_page = RolesPages(driver)
        HeaderPage(driver).open_users()
        UsersPage(driver).click_on_manage_roles()
        roles_page.click_edit_for_default_role()
        roles_page.edit_default_role_to_have_permission(permission)
        Shared(driver).click_submit()

    @then("I reset the permissions")
    def reset_permissions(driver):
        roles_page = RolesPages(driver)
        HeaderPage(driver).open_users()
        UsersPage(driver).click_on_manage_roles()
        roles_page.click_edit_for_default_role()
        roles_page.remove_all_permissions_from_default_role()
        Shared(driver).click_submit()

    @then('I see an ultimate end user')
    def i_see_ultimate_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_ueu_table()
        destinations_table_lower = destinations_table.lower()
        assert "name" in destinations_table_lower
        assert "type" in destinations_table_lower
        assert "website" in destinations_table_lower
        assert "address" in destinations_table_lower
        assert context.ueu_type.lower() in destinations_table.lower()
        assert context.ueu_name.lower() in destinations_table.lower()
        assert context.ueu_website.lower() in destinations_table.lower()
        assert context.ueu_address.lower() in destinations_table.lower()

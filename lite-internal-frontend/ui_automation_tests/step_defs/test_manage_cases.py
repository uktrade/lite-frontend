import re
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.application_page import ApplicationPage
from pages.record_decision_page import RecordDecision
from pages.shared import Shared
from pages.exporter_hub import ExporterHub
import helpers.helpers as utils

from ui_automation_tests.pages.roles_pages import RolesPages

from pages.header_page import HeaderPage
from ui_automation_tests.pages.users_page import UsersPage


class ManageCases():
    scenarios('../features/manage_cases.feature', strict_gherkin=False)

    import logging
    log = logging.getLogger()
    console = logging.StreamHandler()
    log.addHandler(console)


    @when('I click progress application')
    def click_post_note(driver):
        application_page = ApplicationPage(driver)
        application_page.click_progress_application()


    @when('I click record decision')
    def click_post_note(driver, context):
        application_page = ApplicationPage(driver)
        application_page.click_record_decision()
        context.decision_array = []


    @when(parsers.parse('I "{grant_or_deny}" application'))
    def grant_or_deny_decision(driver, grant_or_deny):
        record = RecordDecision(driver)
        if grant_or_deny == "grant":
            record.click_on_grant_licence()
        elif grant_or_deny == "deny":
            record.click_on_deny_licence()

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

    @then(parsers.parse('I see application "{grant_or_deny}"'))
    def see_application_granted_or_denied(driver, grant_or_deny, context):
        record = RecordDecision(driver)
        details = driver.find_elements_by_css_selector(".lite-heading-s")
        for header in details:
            if header.text == "STATUS":
                status_detail = header.find_element_by_xpath("./following-sibling::p").text
                if grant_or_deny == "granted":
                    assert status_detail == "Approved"
                elif grant_or_deny == "denied":
                    assert status_detail == "Under final review"
                    try:
                        context.optional_text
                        assert record.get_text_of_denial_reasons_headers(1) == "Further information"
                        assert record.get_text_of_denial_reasons_listed(6) == context.optional_text
                    except AttributeError:
                        pass
                    except IndexError:
                        pass
                    assert record.get_text_of_denial_reasons_headers(0) == "This case was denied because"
                    # TODO ask dev to put a selector in here
                    i = 5
                    for denial_reason_code in context.decision_array:
                        assert record.get_text_of_denial_reasons_listed(i) == denial_reason_code
                        i += 1

    @when(parsers.parse('I select status "{status}" and save'))
    def select_status_save(driver, status, context):
        application_page = ApplicationPage(driver)
        application_page.select_status(status)
        context.status = status
        context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
        driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]").click()

    @then('the status has been changed in the application')
    def status_has_been_changed_in_header(driver, context):
        application_page = ApplicationPage(driver)
        for header in application_page.get_text_of_application_headings():
            if header.text == "STATUS":
                status_detail = header.find_element_by_xpath("./following-sibling::p").text
                assert status_detail == context.status, "status has not been updated"
        # this also tests that the activities are in reverse chronological order as it is expecting the status change to be first.
        assert context.status.lower() in application_page.get_text_of_case_note_subject(0)
        is_date_in_format = re.search("([0-9]{1,2}):([0-9]{2})(am|pm) ([0-9][0-9]) (January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]{4,})", application_page.get_text_of_activity_dates(0))
        assert is_date_in_format, "date is not displayed after status change"
        assert application_page.get_text_of_activity_users(0) == "first-name last-name", "user who has made the status change has not been displayed correctly"


    #TODO exporter dependency
    @when('I click applications')
    def i_click_applications(driver):
        exporter = ExporterHub(driver)
        exporter.click_applications()


    @then('the status has been changed in exporter')
    def i_click_applications(driver, context):
        elements = driver.find_elements_by_css_selector(".govuk-table__row")
        no = utils.get_element_index_by_text(elements, context.app_time_id)
        assert context.status in elements[no].text


    @then('the application headers and information are correct')
    def application_headers_and_info_are_correct(driver, context):
        assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[0].text == "APPLICANT"
        assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[1].text == "ACTIVITY"
        assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[2].text == "CREATED AT"
        assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[3].text == "REFERENCE NUMBER"
        assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[4].text == "LICENCE TYPE"
        assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[5].text == "LAST UPDATED"
        #  this is hard coded from the organisation that is created as part of setup
        assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[0].text == "Unicorns Ltd"
        assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[1].text == "Trading" or driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[1].text == "Brokering"
        #TODO commented out below line due to bug LT-1281
        #assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[2].text == context.date_time_of_update
        assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[3].text == "None"
        assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[4].text == "Standard licence"

    @when(parsers.parse('I give myself the required permissions for "{permission}"'))
    def get_required_permissions(driver, permission):
        roles_page = RolesPages(driver)
        user_page = UsersPage(driver)
        header = HeaderPage(driver)
        shared = Shared(driver)
        header.open_users()
        user_page.click_on_manage_roles()
        roles_page.click_edit_for_default_role()
        roles_page.edit_default_role_to_have_permission(permission)
        shared.click_submit()

    @then("I reset the permissions")
    def reset_permissions(driver):
        roles_page = RolesPages(driver)
        user_page = UsersPage(driver)
        header = HeaderPage(driver)
        shared = Shared(driver)
        header.open_users()
        user_page.click_on_manage_roles()
        roles_page.click_edit_for_default_role()
        roles_page.remove_all_permissions_from_default_role()
        shared.click_submit()

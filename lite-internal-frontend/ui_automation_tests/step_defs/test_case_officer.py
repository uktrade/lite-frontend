from pytest_bdd import then, scenarios, when

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.case_officer_pages import CaseOfficerPages
from ui_automation_tests.shared import functions

scenarios("../features/case_officer.feature", strict_gherkin=False)


@when("I click Assign Case Officer Button")
def i_click_case_officer_button(driver):
    application_page = ApplicationPage(driver)
    application_page.click_case_officer_button()


@when("filter by test user email")
def filter_users_found(driver, internal_info):
    case_officer_page = CaseOfficerPages(driver)
    case_officer_page.search(internal_info["email"])


@then("I should see one user with the test user name")
def one_user_found(driver, internal_info):
    case_officer_page = CaseOfficerPages(driver)
    emails = case_officer_page.get_users_email()
    assert len(emails) > 0
    for email in emails:
        assert internal_info["email"] in email.text


@when("I click the user and assign")
def click_user_and_assign(driver):
    case_officer_page = CaseOfficerPages(driver)
    case_officer_page.select_first_user()
    functions.click_submit(driver)


@then("I see a case officer is assigned")
def case_officer_is_set(driver, internal_info):
    assert internal_info["name"] in CaseOfficerPages(driver).get_current_case_officer()


@then("I see no case officer is assigned")
def no_case_officer_is_set(driver, internal_info):
    assert internal_info["name"] not in CaseOfficerPages(driver).get_current_case_officer()


@when("I click unassign")
def unassign_case_officer(driver):
    CaseOfficerPages(driver).click_unassign()

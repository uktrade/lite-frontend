from pytest_bdd import then, scenarios, when

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.case_officer_pages import CaseOfficerPages
from ui_automation_tests.shared.fixtures.core import internal_info

scenarios("../features/case_officer.feature", strict_gherkin=False)


@when("I click Assign Case Officer Button")
def i_click_case_officer_button(driver):
    application_page = ApplicationPage(driver)
    application_page.click_case_officer_button()


@when("filter by test user name")
def filter_users_found(driver, internal_info):
    case_officer_page = CaseOfficerPages(driver)
    case_officer_page.search(internal_info["name"])


@then("I should see one user with the test user name")
def one_user_found(driver, internal_info):
    case_officer_page = CaseOfficerPages(driver)
    names = case_officer_page.get_users_name()
    assert len(names) > 0
    for name in names:
        assert internal_info["name"] in name.text


@when("I click the user and assign")
def click_user_and_assign(driver):
    case_officer_page = CaseOfficerPages(driver)
    case_officer_page.select_first_user()
    case_officer_page.click_assign()


@then("I see a case officer is assigned")
def case_officer_is_set(driver):
    assert CaseOfficerPages(driver).is_current_case_officer()


@then("I see no case officer is assigned")
def no_case_officer_is_set(driver):
    assert not CaseOfficerPages(driver).is_current_case_officer()


@when("I click unassign")
def unassign_case_officer(driver):
    CaseOfficerPages(driver).click_unassign()

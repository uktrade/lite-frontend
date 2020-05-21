from pytest_bdd import when, scenarios, then

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.case_list_page import CaseListPage
from ui_automation_tests.pages.case_page import CasePage
from ui_automation_tests.pages.shared import Shared

scenarios("../features/enforcement.feature", strict_gherkin=False)


@when("I click export enforcement xml")
def export_enforcement_xml(driver):
    CaseListPage(driver).click_export_enforcement_xml()


@then("the enforcement check is audited")
def enforcement_audit(driver, internal_url, context):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    assert "exported the case for enforcement check" in Shared(driver).get_audit_trail_text()

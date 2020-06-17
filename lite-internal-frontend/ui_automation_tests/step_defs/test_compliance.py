from datetime import date

from pytest_bdd import when, then, parsers, scenarios, given

from pages.advice import UserAdvicePage, FinalAdvicePage, TeamAdvicePage, BaseAdvicePage
from pages.case_page import CasePage, CaseTabs
from pages.give_advice_pages import GiveAdvicePages
from pages.record_decision_page import RecordDecision
from pages.shared import Shared

from ui_automation_tests.pages.compliance_pages import CompliancePages
from ui_automation_tests.pages.generate_document_page import GeneratedDocument
from ui_automation_tests.pages.grant_licence_page import GrantLicencePage

scenarios("../features/compliance.feature", strict_gherkin=False)


@when("I generate a decision document")  # noqa
def generate_decision_document(driver, context):  # noqa
    generate_document_page = GeneratedDocument(driver)
    generate_document_page.select_generate_document()
    generate_document_page.select_document_template()
    Shared(driver).click_submit()
    Shared(driver).click_submit()
    Shared(driver).click_submit()

    context.status = "finalised"


@when("I go to the compliance case created")  # noqa
def go_to_compliance_case(driver, internal_url, context, api_test_client):  # noqa
    compliance_case_id = api_test_client.cases.get_compliance_id_for_case(context.case_id)
    driver.get(
        internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + str(compliance_case_id[0])
    )


@when("I click on the licences tab")  # noqa
def i_click_on_licences(driver, context):  # noqa
    CasePage(driver).change_tab(CaseTabs.COMPLIANCE_LICENCES)


@then("I see my previously created licence")  # noqa
def check_licence_is_present(driver, context):  # noqa
    assert CompliancePages(driver).find_case_reference(context).text == context.reference_code


@when("I search for the finalised licence")  # noqa
def i_search_for_licence(driver, context):  # noqa
    CompliancePages(driver).filter_by_case_reference(context)

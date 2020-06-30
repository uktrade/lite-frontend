from pytest_bdd import when, then, parsers, scenarios

from pages.case_page import CasePage, CaseTabs
from pages.shared import Shared

from core.builtins.custom_tags import str_date_only
from ui_automation_tests.pages.compliance_pages import CompliancePages
from ui_automation_tests.pages.ecju_queries_pages import EcjuQueriesPages
from ui_automation_tests.pages.generate_document_page import GeneratedDocument

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


@when("I click add a visit report")  # noqa
def add_visit_report(driver):  # noqa
    CompliancePages(driver).add_visit_report()


@then("I am on a compliance visit case")
def on_compliance_case(driver):
    reference = CasePage(driver).get_reference_code_text()
    assert reference.startswith("COMP/")
    assert reference.endswith("/V")


@when(
    parsers.parse("I add I visit report details '{visit_type}', '{visit_date}', '{overall_risk}', and '{licence_risk}'")
)
def add_visit_report_details(driver, context, visit_type, visit_date, overall_risk, licence_risk):
    CompliancePages(driver).add_visit_report_details(visit_type, visit_date, overall_risk, licence_risk)
    context.visit_type = visit_type
    context.visit_date = visit_date
    context.overall_risk = overall_risk
    context.licence_risk = licence_risk


@then("I see the visit report details in details and the banner")
def see_visit_report_details(driver, context):
    compliance_page = CompliancePages(driver)
    assert context.visit_type in compliance_page.get_visit_type()
    assert str_date_only(context.visit_date) in compliance_page.get_visit_date()
    assert context.overall_risk in compliance_page.get_overall_risk()
    assert context.licence_risk in compliance_page.get_licence_risk()

    # Banner details
    assert context.visit_type in compliance_page.get_compliance_banner_details()
    assert str_date_only(context.visit_date) in compliance_page.get_compliance_banner_details()


@when(parsers.parse("I add person present '{name}' who works as '{job}'"))
def add_people_present(driver, context, name, job):
    CompliancePages(driver).add_person_present(name, job)
    context.person_name = name
    context.job_title = job


@then("I see the people present")
def person_is_present(driver, context):
    table = CompliancePages(driver).get_people_present_table()
    assert context.person_name in table
    assert context.job_title in table


@when(parsers.parse("I add overview details of '{details}'"))
def add_overview_details(driver, context, details):
    CompliancePages(driver).edit_overview(details)
    context.overview = details


@then("I see overview details")
def see_overview_details(driver, context):
    assert context.overview in CompliancePages(driver).get_overview()


@when(parsers.parse("I add inspection details of '{details}'"))
def add_inspection_details(driver, context, details):
    CompliancePages(driver).edit_inspection(details)
    context.inspection = details


@then("I see inspection details")
def see_inspection_details(driver, context):
    assert context.inspection in CompliancePages(driver).get_inspection()


@when(parsers.parse("I add Compliance with licences details '{overview}' and '{risk}'"))
def add_compliance_with_licences_details(driver, context, overview, risk):
    CompliancePages(driver).edit_compliance_with_licences(overview, risk)
    context.compliance_overview = overview
    context.compliance_risk = risk


@then("I see Compliance with licences details")
def see_compliance_with_licence_details(driver, context):
    assert context.compliance_overview in CompliancePages(driver).get_compliance_with_licence_overview()
    assert context.compliance_risk in CompliancePages(driver).get_compliance_with_licence_risk()


@when(parsers.parse("I add knowledge of key individuals details '{overview}' and '{risk}'"))
def add_knowledge_of_individuals_details(driver, context, overview, risk):
    CompliancePages(driver).edit_knowledge_of_individuals(overview, risk)
    context.individuals_overview = overview
    context.individuals_risk = risk


@then("I see knowledge of key individuals details")
def see_knowledge_of_individuals_details(driver, context):
    assert context.individuals_overview in CompliancePages(driver).get_knowledge_of_individuals_overview()
    assert context.individuals_risk in CompliancePages(driver).get_knowledge_of_individuals_risk()


@when(parsers.parse("I add knowledge of controlled product details '{overview}' and '{risk}'"))
def add_knowledge_of_products_details(driver, context, overview, risk):
    CompliancePages(driver).edit_knowledge_of_products(overview, risk)
    context.products_overview = overview
    context.products_risk = risk


@then("I see knowledge of controlled product details")
def see_knowledge_of_products_details(driver, context):
    assert context.products_overview in CompliancePages(driver).get_knowledge_of_products_overview()
    assert context.products_risk in CompliancePages(driver).get_knowledge_of_products_risk()


@when("I go to the ECJU queries tab")
def i_go_to_the_ecju_queries_tab(driver):
    CasePage(driver).change_tab(CaseTabs.ECJU_QUERIES)


@then("I see different ecju query buttons")
def see_ecju_query_types(driver):
    ecju_query_page = EcjuQueriesPages(driver)
    assert ecju_query_page.new_query_button_visible()
    assert ecju_query_page.previsit_questionnaire_button_visible()
    assert ecju_query_page.compliance_actions_button_visible()

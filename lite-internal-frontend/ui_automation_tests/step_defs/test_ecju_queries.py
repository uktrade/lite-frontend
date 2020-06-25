from uuid import uuid4

from pytest_bdd import when, then, scenarios, given

from pages.application_page import ApplicationPage
from pages.case_page import CasePage, CaseTabs
from pages.ecju_queries_pages import EcjuQueriesPages
from shared import functions
from ui_automation_tests.pages.shared import Shared

scenarios("../features/ecju_queries.feature", strict_gherkin=False)


@given("I create an ecju query picklist")
def i_create_an_ecju_query_picklist(context, add_an_ecju_query_picklist):
    context.ecju_query_picklist_name = add_an_ecju_query_picklist["name"]
    context.ecju_query_picklist_question_text = add_an_ecju_query_picklist["text"]


@when("I go to the ECJU queries tab")
def i_go_to_the_ecju_queries_tab(driver):
    CasePage(driver).change_tab(CaseTabs.ECJU_QUERIES)


@when("I click new query")
def i_click_add_an_ecju_query(driver):
    EcjuQueriesPages(driver).click_new_query_button()


@when("I enter in my query text")
def i_enter_text_in_the_question_text_area(driver, context):
    ecju_queries_pages = EcjuQueriesPages(driver)
    context.ecju_question = str(uuid4())
    ecju_queries_pages.enter_question_text(context.ecju_question)
    functions.click_submit(driver)


@then("the new ECJU Query is visible in the list")
def the_new_ecju_query_is_visible_in_the_list(driver, context):
    assert context.ecju_question in EcjuQueriesPages(driver).get_open_queries_text()


@then("the ECJU Query creation is visible in the case timeline")
def the_ecju_query_creation_is_visible_in_the_case_timeline(driver, context, internal_url):
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    assert context.ecju_question in Shared(driver).get_audit_trail_text()


@when("I create a response to the ECJU query")
def i_create_a_response_to_an_ecju(driver, context, api_test_client):
    context.ecju_response = str(uuid4())
    api_test_client.ecju_queries.add_ecju_response(question=context.ecju_question, response=context.ecju_response)
    driver.refresh()


@then("the ECJU Query is in the closed list")
def ecju_query_in_closed_list(driver, context):
    CasePage(driver).change_tab(CaseTabs.ECJU_QUERIES)
    assert context.ecju_question in EcjuQueriesPages(driver).get_closed_queries_text()

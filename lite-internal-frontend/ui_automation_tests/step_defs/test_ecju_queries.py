from uuid import uuid4

from pytest_bdd import when, then, scenarios, given

from pages.application_page import ApplicationPage
from pages.ecju_queries_pages import EcjuQueriesPages
from pages.shared import Shared
from shared import functions

scenarios("../features/ecju_queries.feature", strict_gherkin=False)

NEW_QUESTION_DROP_DOWN_TEXT = "Write a new question"


@given("I create an ecju query picklist")
def i_create_an_ecju_query_picklist(context, add_an_ecju_query_picklist):
    context.ecju_query_picklist_name = add_an_ecju_query_picklist["name"]
    context.ecju_query_picklist_question_text = add_an_ecju_query_picklist["text"]


@when("I click the ECJU Queries button")
def i_click_ecju_queries_button(driver):
    application_page = ApplicationPage(driver)
    application_page.click_ecju_queries_button()


@when("I click Add an ECJU Query")
def i_click_add_an_ecju_query(driver):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.click_add_an_ecju_query_btn()


@when("I select a standard ECJU picklist question")
def i_select_standard_picklist_question(driver, context):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.select_ecju_query_type(context.ecju_query_picklist_name)


@then("the question text area contains expected text")
def the_question_text_area_contains_expected_text(driver, context):
    assert context.ecju_query_picklist_question_text == EcjuQueriesPages(driver).get_question_text()


@when("I Select Write a new question")
def i_select_write_a_new_question(driver):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.select_ecju_query_type(NEW_QUESTION_DROP_DOWN_TEXT)


@then("the question text area is empty")
def the_question_text_area_is_empty(driver):
    driver.set_timeout_to(0)
    assert not EcjuQueriesPages(driver).get_question_text()
    driver.set_timeout_to(10)


@when("I enter text in the question text area")
def i_enter_text_in_the_question_text_area(driver, context):
    ecju_queries_pages = EcjuQueriesPages(driver)
    context.ecju_question = str(uuid4())
    ecju_queries_pages.enter_question_text(context.ecju_question)


@when("I click No")
def i_click_no(driver):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.click_confirm_query_create_no()


@then("the question text area contains previously entered text")
def the_question_text_area_contains_expected_text(driver, context):
    assert context.ecju_question == EcjuQueriesPages(driver).get_question_text()


@when("I click Yes")
def i_click_yes(driver):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.click_confirm_query_create_yes()


@then("the new ECJU Query is visible in the list")
def the_new_ecju_query_is_visible_in_the_list(driver, context):
    ecju_queries_pages = EcjuQueriesPages(driver)
    assert context.ecju_question in ecju_queries_pages.get_open_query_questions()


@then("the ECJU Query creation is visible in the case timeline")
def the_ecju_query_creation_is_visible_in_the_case_timeline(driver, context):
    application_page = ApplicationPage(driver)
    assert context.ecju_question in application_page.get_text_of_audit_trail_item(0)


@when("I create a response to the ECJU query")
def i_create_a_response_to_an_ecju(driver, context):
    context.ecju_response = str(uuid4())
    context.api.seed_ecju.add_ecju_response(question=context.ecju_question, response=context.ecju_response)
    driver.refresh()


@then("the ECJU Query is in the closed list")
def ecju_query_in_closed_list(driver, context):
    ecju_page = EcjuQueriesPages(driver)
    assert context.ecju_response in ecju_page.get_closed_query_answers()
    assert context.ecju_question in ecju_page.get_closed_query_questions()


@when("I click back")  # noqa
def i_click_back(driver):
    functions.click_back_link(driver)


@when("I click the case breadcrumb")  # noqa
def i_click_back_the_case_breadcrumb(driver):
    driver.find_element_by_id("link-back-to-case").click()

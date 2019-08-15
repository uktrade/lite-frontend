from uuid import uuid4
from pytest_bdd import when, then, parsers, scenarios, given
from pages.application_page import ApplicationPage
from pages.ecju_queries_pages import EcjuQueriesPages

scenarios('../features/ecju_query.feature', strict_gherkin=False)

NEW_QUESTION_DROP_DOWN_TEXT = 'Write a new question'


@given("I create an ecju query picklist")
def i_create_an_ecju_query_picklist(context, add_an_ecju_query_picklist):
    context.ecju_query_picklist_name = add_an_ecju_query_picklist['name']
    context.ecju_query_picklist_question_text = add_an_ecju_query_picklist['text']


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
    assert not EcjuQueriesPages(driver).get_question_text()


@when("I enter text in the question text area")
def i_enter_text_in_the_question_text_area(driver, context):
    ecju_queries_pages = EcjuQueriesPages(driver)
    context.custom_question_text = str(uuid4())
    ecju_queries_pages.enter_question_text(context.custom_question_text)


@when("I click No")
def i_click_no(driver):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.click_confirm_query_create_no()


@then("the question text area contains previously entered text")
def the_question_text_area_contains_expected_text(driver, context):
    assert context.custom_question_text == EcjuQueriesPages(driver).get_question_text()


@when("I click Yes")
def i_click_yes(driver):
    ecju_queries_pages = EcjuQueriesPages(driver)
    ecju_queries_pages.click_confirm_query_create_yes()


@then("the new ECJU Query is visible in the list")
def the_new_ecju_query_is_visible_in_the_list(driver, context):
    ecju_queries_pages = EcjuQueriesPages(driver)
    assert context.custom_question_text in ecju_queries_pages.get_all_ecju_query_questions()


@then("the ECJU Query creation is visible in the case timeline")
def the_ecju_query_creation_is_visible_in_the_case_timeline(driver, context):
    application_page = ApplicationPage(driver)
    assert context.custom_question_text in application_page.get_text_of_audit_trail_item(0)

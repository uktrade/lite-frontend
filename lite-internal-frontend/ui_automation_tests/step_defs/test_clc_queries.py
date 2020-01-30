from pytest_bdd import when, then, scenarios, given
from pages.clc_queries_pages import ClcQueriesPages
from pages.shared import Shared

from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id

scenarios("../features/clc_queries.feature", strict_gherkin=False)


@when("I click Respond to query")
def respond_to_query(driver):
    ClcQueriesPages(driver).click_respond_to_query()


@when("I submit response")
def submit_response(driver):
    scroll_to_element_by_id(driver, ClcQueriesPages.SUBMIT_RESPONSE_BUTTON_ID)
    Shared(driver).click_submit()


@then("I see case is closed")
def check_case_closed(driver):
    assert ClcQueriesPages(driver).is_clc_query_case_closed()


@when("I go to clc query previously created")  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/cases/" + context.clc_case_id)


@given("I create a clc query")  # noqa
def create_clc_query(driver, apply_for_clc_query, context):
    pass

from pytest_bdd import when, then, scenarios, given, parsers
from pages.goods_queries_pages import GoodsQueriesPages
from pages.shared import Shared

from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id

scenarios("../features/goods_queries.feature", strict_gherkin=False)


@when("I click Respond to clc query")
def respond_to_query(driver):
    GoodsQueriesPages(driver).click_respond_to_clc_query()


@when("I click Respond to grading query")
def respond_to_query(driver):
    GoodsQueriesPages(driver).click_respond_to_grading_query()


@when("I submit response")
def submit_response(driver):
    scroll_to_element_by_id(driver, GoodsQueriesPages.SUBMIT_RESPONSE_BUTTON_ID)
    GoodsQueriesPages(driver).click_overview_submit()


@then("I see case is closed")
def check_case_closed(driver):
    assert GoodsQueriesPages(driver).is_clc_query_case_closed()


@when("I go to goods query previously created")  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/cases/" + context.clc_case_id)


@given("I create a grading query")  # noqa
def create_grading_query(driver, apply_for_grading_query, context):
    pass


@when(  # noqa
    parsers.parse(
        'I respond prefix "{prefix}", select "{grading}", suffix "{suffix}", comment "{comment}", and click continue'
    )  # noqa
)  # noqa
def enter_response(driver, prefix, grading, suffix, comment):  # noqa
    clc_query_page = GoodsQueriesPages(driver)
    clc_query_page.enter_a_prefix(prefix)
    clc_query_page.select_a_grading(grading)
    clc_query_page.enter_a_suffix(suffix)
    clc_query_page.enter_a_comment(comment)
    Shared(driver).click_submit()

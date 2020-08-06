from pytest_bdd import when, then, scenarios, given, parsers

from pages.application_page import ApplicationPage
from pages.goods_queries_pages import GoodsQueriesPages
from pages.shared import Shared

scenarios("../features/goods_queries.feature", strict_gherkin=False)


@when("I click Respond to clc query")
def respond_to_query(driver):
    GoodsQueriesPages(driver).click_respond_to_clc_query()


@when("I click Respond to grading query")
def respond_to_query(driver):
    GoodsQueriesPages(driver).click_respond_to_grading_query()


@then("I see case is closed")
def check_case_closed(driver):
    assert GoodsQueriesPages(driver).is_clc_query_case_closed()


@when("I go to goods query previously created")  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.clc_case_id)


@when("I go to pv goods query previously created")  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.pv_case_id)


@given("I create a grading query")  # noqa
def create_grading_query(driver, apply_for_grading_query, context):
    pass


@when(  # noqa
    parsers.parse(
        'I respond prefix "{prefix}", select "{grading}", suffix "{suffix}", comment "{comment}", and click submit'
    )  # noqa
)  # noqa
def enter_response(driver, prefix, grading, suffix, comment):  # noqa
    clc_query_page = GoodsQueriesPages(driver)
    clc_query_page.enter_a_prefix(prefix)
    clc_query_page.select_a_grading(grading)
    clc_query_page.enter_a_suffix(suffix)
    clc_query_page.enter_a_comment(comment)
    Shared(driver).click_submit()


@then("the status has been changed in the pv query")  # noqa
def audit_trail_updated(driver, context, internal_info, internal_url):  # noqa
    ApplicationPage(driver).go_to_cases_activity_tab_for_pv(internal_url, context)

    assert (
        context.status.lower() in Shared(driver).get_audit_trail_text().lower()
    ), "status has not been shown as approved in audit trail"


@then("the status has been changed in the clc query")  # noqa
def audit_trail_updated(driver, context, internal_info, internal_url):  # noqa
    ApplicationPage(driver).go_to_cases_activity_tab_for_clc(internal_url, context)

    assert (
        context.status.lower() in Shared(driver).get_audit_trail_text().lower()
    ), "status has not been shown as approved in audit trail"

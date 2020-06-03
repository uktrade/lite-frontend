from pages.case_page import CasePage
from pages.goods_queries_pages import GoodsQueriesPages
from pytest_bdd import when, then, scenarios, parsers
from pages.application_page import ApplicationPage
from pages.shared import Shared


scenarios("../features/review_goods.feature", strict_gherkin=False)


@when("I select good and click review")
def click_edit_flags_link(driver):
    CasePage(driver).select_first_good()
    ApplicationPage(driver).click_review_goods()


@when(parsers.parse('I respond "{controlled}", "{control_list_entry}", "{report}", "{comment}" and click submit'))
def click_continue(driver, controlled, control_list_entry, report, comment, context):
    query_page = GoodsQueriesPages(driver)
    query_page.click_is_good_controlled(controlled)
    query_page.type_in_to_control_list_entry(control_list_entry)
    context.goods_control_list_entry = control_list_entry
    query_page.choose_report_summary()
    context.report = report
    query_page.enter_a_comment(comment)
    context.comment = comment
    Shared(driver).click_submit()


@then("the control list is present on the case page")
def check_control_list_code(driver, context):
    goods = CasePage(driver).get_goods_text()
    assert context.goods_control_list_entry in goods

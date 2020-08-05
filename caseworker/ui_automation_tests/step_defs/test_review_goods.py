from pytest_bdd import when, then, scenarios

from pages.application_page import ApplicationPage
from pages.case_page import CasePage

scenarios("../features/review_goods.feature", strict_gherkin=False)


@when("I select good and click review")
def click_edit_flags_link(driver):
    CasePage(driver).select_first_good()
    ApplicationPage(driver).click_review_goods()


@then("the control list is present on the case page")
def check_control_list_code(driver, context):
    goods = CasePage(driver).get_goods_text()
    assert context.goods_control_list_entry in goods

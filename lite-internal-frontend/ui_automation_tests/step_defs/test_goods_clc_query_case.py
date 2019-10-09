from pytest_bdd import scenarios, when, then

from pages.application_page import ApplicationPage
from pages.case_list_page import CaseListPage
from pages.shared import Shared

scenarios('../features/add_goods.feature', strict_gherkin=False)


@then('I see the clc-case previously created') # noqa
def assert_case_is_present(driver, apply_for_clc_query, context):
    assert CaseListPage(driver).assert_case_is_present(context.clc_case_id), "clc case ID is not present on page"


@when("I click on good")
def click_good(driver):
    ApplicationPage(driver).click_good_description_link()


@then("I see good information")
def good_info(driver):
    assert Shared(driver).info_board_is_displayed()

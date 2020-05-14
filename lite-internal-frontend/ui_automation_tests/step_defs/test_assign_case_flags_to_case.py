from pytest_bdd import when, then, scenarios

from pages.application_page import ApplicationPage
from pages.case_page import CasePage

scenarios("../features/assign_case_flags_to_case.feature", strict_gherkin=False)


@when("I click edit flags on the first destination")
def click_edit_destination_flags_link(driver):
    case_page = CasePage(driver)
    case_page.select_destination(0)
    case_page.click_edit_destinations_flags()


@when("I click edit flags on the first good")
def click_edit_goods_flags_link(driver):
    case_page = CasePage(driver)
    case_page.select_first_good()
    case_page.click_edit_goods_flags()


@then("the previously created goods flag is assigned to the good")
def assert_flag_is_assigned(driver, context):
    assert CasePage(driver).is_goods_flag_applied(context.flag_name)


@then("I see 3 flags for the case")
def three_out_of_text(driver, context):
    case_row = driver.find_element_by_id(context.case_id)
    assert "(3 of " in case_row.text


@then("I see all flags for the case")
def dont_see_three_out_of(driver, context):
    case_row = driver.find_element_by_id(context.case_id)
    assert "(3 of " not in case_row.text


@when("I click the expand flags dropdown")  # noqa
def click_chevron(driver, context):
    ApplicationPage(driver).click_expand_flags(context.case_id)

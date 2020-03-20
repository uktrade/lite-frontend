from pytest_bdd import when, then, scenarios

from pages.application_page import ApplicationPage

scenarios("../features/assign_case_flags_to_case.feature", strict_gherkin=False)


@when("I click edit flags link")
def click_edit_case_flags_link(driver):
    ApplicationPage(driver).click_edit_case_flags()


@when("I click edit destination flags link")
def click_edit_destination_flags_link(driver):
    ApplicationPage(driver).click_edit_destination_flags()


@when("I click edit goods flags link")
def click_edit_goods_flags_link(driver):
    application_page = ApplicationPage(driver)
    application_page.select_a_good()
    application_page.click_edit_good_flags()


@then("The previously created flag is assigned to the case")
def assert_flag_is_assigned(driver, context):
    application_page = ApplicationPage(driver)
    exists = application_page.is_flag_applied(context.flag_name)
    assert exists is True


@then("the previously created goods flag is assigned to the case")
def assert_flag_is_assigned(driver, context):
    assert ApplicationPage(driver).is_good_flag_applied(context.flag_name)


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

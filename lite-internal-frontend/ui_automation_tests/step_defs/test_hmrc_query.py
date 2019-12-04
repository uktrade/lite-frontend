from pytest_bdd import given, scenarios, when, then

from pages.case_list_page import CaseListPage

scenarios("../features/hmrc_query.feature", strict_gherkin=False)


@given("I create a hmrc query")  # noqa
def create_hmrc_query(driver, apply_for_hmrc_query, context):
    pass


@when("I go to HMRC query")  # noqa
def go_to_hmrc(driver, context):
    driver.set_timeout_to(0)
    context.hmrc_is_found = False
    if len(driver.find_elements_by_css_selector('.govuk-table__body .govuk-link[href*="cases"]')) > 0:
        context.hmrc_is_found = True
        driver.find_element_by_css_selector('.govuk-table__body .govuk-link[href*="cases"]').click()
    driver.set_timeout_to(10)


@then("I see HMRC query")
def see_hmrc(driver, context):
    if context.hmrc_is_found:
        assert driver.find_element_by_css_selector(".govuk-caption-m").text == "HMRC Query"

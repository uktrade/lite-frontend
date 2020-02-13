from pytest_bdd import scenarios, when, then

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.shared import functions

scenarios("../features/hmrc_query.feature", strict_gherkin=False)


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
        assert driver.find_element_by_id("case-type").text == "HMRC Query"
        assert functions.element_with_id_exists(driver, ApplicationPage(driver).HMRC_GOODS_LOCATION)

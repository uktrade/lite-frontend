from pytest_bdd import given, scenarios, when, then

from pages.case_list_page import CaseListPage

scenarios("../features/hmrc_query.feature", strict_gherkin=False)


@given("I create a hmrc query")  # noqa
def create_hmrc_query(driver, apply_for_hmrc_query, context):
    pass


@when("I go to HMRC query")  # noqa
def go_to_hmrc(driver):
    driver.find_element_by_css_selector('.govuk-link[href*="cases"]').click()


@then("I see HMRC query")
def see_hmrc(driver):
    assert driver.find_element_by_css_selector(".govuk-caption-m").text == "HMRC Query"

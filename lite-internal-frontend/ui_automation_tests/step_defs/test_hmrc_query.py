from pytest_bdd import scenarios, when, then, given

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.shared import functions

scenarios("../features/hmrc_query.feature", strict_gherkin=False)


@given("I create HMRC query")
def create_hmrc(apply_for_hmrc_query):
    pass


@when("I go to HMRC query previously created")
def go_to_hmrc(driver, internal_url, context):
    driver.get(internal_url.rstrip("/") + "/cases/" + context.case_id)


@then("I see HMRC query")
def see_hmrc(driver, context):
    assert driver.find_element_by_id("case-type").text == "HMRC Query"
    assert functions.element_with_id_exists(driver, ApplicationPage(driver).HMRC_GOODS_LOCATION)

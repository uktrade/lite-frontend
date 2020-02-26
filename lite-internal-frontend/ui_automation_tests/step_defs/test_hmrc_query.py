from pytest_bdd import scenarios, then, given

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.shared import functions

scenarios("../features/hmrc_query.feature", strict_gherkin=False)


@given("I create HMRC query")
def create_hmrc(apply_for_hmrc_query):
    pass


@then("I see HMRC query")
def see_hmrc(driver, context):
    assert ApplicationPage(driver).get_type_of_case_from_page() == "HMRC Query"
    assert functions.element_with_id_exists(driver, ApplicationPage(driver).HMRC_GOODS_LOCATION)

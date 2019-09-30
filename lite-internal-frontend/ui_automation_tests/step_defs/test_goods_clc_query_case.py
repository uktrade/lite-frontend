from pytest_bdd import scenarios, when, then
from pages.case_list_page import CaseListPage

scenarios('../features/add_goods.feature', strict_gherkin=False)


@then('I see the clc-case previously created') # noqa
def assert_case_is_present(driver, apply_for_clc_query, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.clc_case_id), "clc case ID is not present on page"


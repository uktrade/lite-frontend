from pytest_bdd import scenarios, then

from pages.case_list_page import CaseListPage

scenarios("../features/goods_clc_query_case.feature", strict_gherkin=False)


@then("I see the clc-case previously created")  # noqa
def assert_case_is_present(driver, apply_for_clc_query, context):
    assert CaseListPage(driver).assert_case_is_present(context.clc_case_id), "clc case ID is not present on page"

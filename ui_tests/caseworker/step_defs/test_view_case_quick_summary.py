from pytest_bdd import scenarios, then

from selenium.webdriver.common.by import By

scenarios("../features/view_case_quick_summary.feature", strict_gherkin=False)


@then("I see the quick summary")  # noqa
def quick_summary_visible(driver, context):
    assert driver.find_element(by=By.TAG_NAME, value="h2").text == "Quick summary"
    end_use_on_page = driver.find_element(by=By.ID, value="quick-summary__end-use").text
    assert "intended end use" in end_use_on_page

import pytest

from pytest_bdd import scenarios, when, then

from selenium.webdriver.common.by import By

scenarios("../features/view_goods.feature", strict_gherkin=False)


@pytest.fixture
def good_name(context):
    return context.goods[0]["good"]["name"]


@when("I click the first good on the case")  # noqa
def click_good_on_case(driver, good_name):
    driver.find_element(
        by=By.LINK_TEXT,
        value=good_name,
    ).click()


@then("I see the good details")  # noqa
def good_details_visible(driver, good_name):
    assert driver.find_element(by=By.TAG_NAME, value="h2").text == "Product details"
    assert driver.find_element(by=By.CSS_SELECTOR, value="div.govuk-caption-l").text == good_name

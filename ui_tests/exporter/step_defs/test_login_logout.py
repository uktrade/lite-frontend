from django.conf import settings

from pytest_bdd import scenarios, then, parsers, when

from selenium.webdriver.common.by import By

scenarios("../features/login_logout.feature", strict_gherkin=False)


@then(parsers.parse('page title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


@when("I click the logout link")
def click_the_logout_link(driver):
    driver.find_element(by=By.LINK_TEXT, value="Sign out").click()


@then("I am taken to the GOV UK page")
def taken_to_the_gov_uk_page(driver):
    heading = driver.find_element(by=By.CSS_SELECTOR, value="h1").text.strip()
    assert heading == "Apply for a standard individual export licence (SIEL)"

    SIGN_IN_BUTTON_ID = "button-sign-in"
    sign_in_button = driver.find_element(by=By.ID, value=SIGN_IN_BUTTON_ID)
    assert sign_in_button

    if not settings.MOCK_SSO_ACTIVATE_ENDPOINTS:
        # With the mock SSO clicking sign in is just going to take us straight
        # to the logged in dashboard so there's no need to check this
        # interstitial page.
        sign_in_button.click()
        assert "signin" in driver.current_url

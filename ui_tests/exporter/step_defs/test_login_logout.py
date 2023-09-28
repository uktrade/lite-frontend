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
def taken_to_the_great_page(driver, settings):
    SIGN_IN_BUTTON_ID = "button-sign-in"
    driver.find_element(by=By.ID, value=SIGN_IN_BUTTON_ID).click()
    if not settings.MOCK_SSO_ACTIVATE_ENDPOINTS:
        # The GovUK One SSO URLS look like signin.X.Y.gov.uk
        assert "signin" in driver.current_url
    else:
        # Using the mock_sso is a little different - clicking "sign in" will take us to
        # select-organisation (and sign in the user)
        assert driver.current_url == f"{settings.AUTHBROKER_URL}select-organisation/"
        # This is a step ahead of the real SSO: it has actually signed in, so sign out.
        driver.find_element(by=By.LINK_TEXT, value="Sign out").click()

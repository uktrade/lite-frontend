from pytest_bdd import scenarios, then, parsers

scenarios('../features/login.feature', strict_gherkin=False)


@then(parsers.parse('driver title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text

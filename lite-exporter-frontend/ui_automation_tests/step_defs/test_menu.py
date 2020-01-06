from pytest_bdd import scenarios, then, when

scenarios("../features/menu.feature", strict_gherkin=False)


@then("the log out link is displayed")
def log_out_link_displayed(driver):
    assert driver.find_element_by_id(
        "link-sign-out"
    ).is_displayed(), "Log out button is not displayed. User may have the service unavailable screen."


@when("I refresh the page")
def refresh(driver):
    driver.refresh()

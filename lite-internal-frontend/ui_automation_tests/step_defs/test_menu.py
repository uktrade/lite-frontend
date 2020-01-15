from pytest_bdd import scenarios, then, when

from pages.header_page import HeaderPage

scenarios("../features/menu.feature", strict_gherkin=False)


@then("the log out link is displayed")
def success(driver):
    assert driver.find_element_by_id(
        "link-log-out"
    ).is_displayed(), "Log out button is displayed. User may have the service unavailable screen."


@when("I refresh the page")
def refresh(driver):
    driver.refresh()


@when("I go to organisations via menu")
def i_go_to_organisations(driver, context):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_organisations()
    context.org_registered_status = False


@when("I go to teams via menu")
def go_to_teams_via_menu(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_teams()


@when("I go to My Team via menu")
def i_go_to_my_team(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_my_team()


@when("I go to queues via menu")  # noqa
def go_to_queues_via_menu(driver):
    HeaderPage(driver).click_lite_menu()
    HeaderPage(driver).click_queues()


@when("I go to flags via menu")  # noqa
def go_to_flags_menu(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_flags()


@when("I go to users via menu")  # noqa
def go_to_users(driver):
    header = HeaderPage(driver)
    header.open_users()


@when("I go to letters via menu")
def go_to_letters(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_letters()


@when("I go to HMRC via menu")
def i_go_to_hmrc(driver, context):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_hmrc()
    context.org_registered_status = False

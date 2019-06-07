from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
import helpers.helpers as utils
from pages.exporter_hub_page import ExporterHubPage
scenarios('../features/add_users_setup.feature')

@when('I click on the users link')
def click_users_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_users()


@then('I add a user')
def add_user(driver):
    exporter_hub = ExporterHubPage(driver)
    exists = utils.is_element_present(driver, By.XPATH, "//td[text()[contains(.,'testuser_1@mail.com')]]")
    if not exists:
        for x in range(3):
            i = str(x + 1)
            exporter_hub.click_add_a_user_btn()
            exporter_hub.enter_first_name("Test")
            exporter_hub.enter_last_name("user_" + i)
            exporter_hub.enter_email("testuser_" + i + "@mail.com")
            exporter_hub.enter_password("1234")
            exporter_hub.click_save_and_continue()

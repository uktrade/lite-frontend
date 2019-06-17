from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from pages.internal_hub_page import InternalHubPage
import helpers.helpers as utils
scenarios('../features/manage_cases.feature')


@when('I manage cases')
def manage_cases(driver):
    internal_hub = InternalHubPage(driver)

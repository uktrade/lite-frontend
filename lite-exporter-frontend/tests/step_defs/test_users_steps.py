import datetime
import time
from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.hub_page import Hub
from pages.shared import Shared
from conftest import context
import helpers.helpers as utils


scenarios('../features/manage_users.feature', strict_gherkin= False)


@when('I click on users')
def click_users(driver):
    hub_page = Hub(driver)
    hub_page.click_on_users_button()


@when('I add a new user')
def add_new_user(driver, first_name, last_name, password):
    hub_page = Hub(driver)
    hub_page.click_add_user_button()
    user_id = datetime.datetime.now().strftime("%m%d%H%M")
    last_name = last_name + user_id
    context.name = first_name + " " + last_name
    hub_page.enter_first_name(first_name)
    hub_page.enter_last_name(last_name)
    email = first_name + last_name + "@mail.com"
    context.email = email
    hub_page.enter_first_name(first_name)
    hub_page.enter_last_name(last_name)
    hub_page.enter_email(email)
    hub_page.enter_password(password)
    driver.find_element_by_css_selector('button[type*="submit"]').click()


@then('I see the manage user screen')
def manage_users_screen(driver):
    assert utils.is_element_present(driver, By.XPATH,
                                    "//td[text()='" + context.email + "']/following-sibling::td[text()='active']")

    assert driver.find_element_by_tag_name("h1").text == "Users", \
        "Failed to return to Users list page after Adding user"


@when('I click edit user')
def click_edit_user(driver):
    element = driver.find_element_by_xpath(
        "//*[text()[contains(.,'" + context.name + "')]]/following-sibling::td[last()]/a")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(1)
    element.click()


@when('I edit user')
def edit_user(driver, first_name, last_name):
    hub_page = Hub(driver)
    context.edited_first_name = first_name + "_edited_"
    context.edited_last_name = last_name + "_edited_"
    context.edited_email = "edited_" + context.email
    hub_page.enter_first_name(edited_first_name)
    hub_page.enter_last_name(last_name + "_edited_")
    hub_page.enter_email("edited_" + context.email)
    driver.find_element_by_css_selector('button[type*="submit"]').click()

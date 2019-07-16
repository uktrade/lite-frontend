from pytest_bdd import scenarios, when, parsers, then
from conftest import context
from pages.users_page import UsersPage
from pages.roles_pages import RolesPages
from pages.shared import Shared

import helpers.helpers as utils


from pages.header_page import HeaderPage

scenarios('../features/roles.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I go to users')
def go_to_flags(driver):
    header = HeaderPage(driver)

    header.open_users()


@when('I go to manage roles')
def go_to_manage_roles(driver):
    user_page = UsersPage(driver)

    user_page.click_on_manage_roles()

@when(parsers.parse('I add a new role called "{role_name}" with permission to "{permissions}"'))
def add_a_role(driver, role_name, permissions):
    roles_page = RolesPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()

    roles_page.click_add_a_role_button()
    if role_name == " ":
        context.role_name = role_name
    else:
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string))-14:]
        context.role_name = role_name + extra_string

    roles_page.enter_role_name(context.role_name)
    roles_page.select_permissions(permissions)
    shared.click_submit()


@then('I see the role in the roles list')
def see_role_in_list(driver):
    role_name = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.role_name + "')]]")
    assert role_name.is_displayed()


@when('I add an existing role name')
def add_existing_flag(driver):
    roles_pages = RolesPages(driver)
    shared = Shared(driver)
    roles_pages.click_add_a_role_button()
    roles_pages.enter_role_name(context.role_name)
    shared.click_submit()


@when('I edit my role')
def edit_existing_role(driver):
    elements = driver.find_elements_by_css_selector(".lite-table__cell")
    no = 0
    while no < len(elements):
        if elements[no].text == context.role_name:
            element_number = no
        no += 1

    elements[element_number + 2].find_element_by_css_selector("a").click()
    roles_pages = RolesPages(driver)
    context.flag_name = str(context.role_name)[:12] + "edited"
    roles_pages.enter_role_name(context.role_name)
    driver.find_element_by_css_selector("[type*='submit']").click()



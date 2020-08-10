from pytest_bdd import scenarios, when, parsers, then

from ui_tests.exporter.pages.roles_pages import RolesPages
from ui_tests.exporter.pages.shared import Shared
import tests_common.tools.helpers as utils
from tests_common import functions

scenarios("../features/roles.feature", strict_gherkin=False)


@when("I go to manage roles")
def go_to_manage_roles(driver):
    manage_hub = RolesPages(driver)
    manage_hub.click_on_manage_roles()


@when(parsers.parse('I add a new role with permission to "{permissions}"'))
def add_a_role(driver, permissions, context):
    roles_page = RolesPages(driver)
    roles_page.click_add_a_role_button()
    context.role_name = "test-" + str(utils.get_unformatted_date_time())[:25]
    roles_page.enter_role_name(context.role_name)
    roles_page.select_permissions(permissions)
    functions.click_submit(driver)


@then("I see the role in the roles list")
def see_role_in_list(driver, context):
    assert RolesPages(driver).find_role_row(context.role_name)


@when("I edit my role")
def edit_existing_role(driver, context):
    roles_page = RolesPages(driver)
    roles_page.click_edit_role(context.role_name)
    context.role_name = str(context.role_name)[:22] + " edited"
    roles_page.enter_role_name(context.role_name)
    functions.click_submit(driver)

from pytest_bdd import scenarios, when, parsers, then

from pages.roles_pages import RolesPages
from pages.shared import Shared
import shared.tools.helpers as utils
from shared import functions

scenarios("../features/roles.feature", strict_gherkin=False)


@when("I go to manage roles")
def go_to_manage_roles(driver):
    manage_hub = RolesPages(driver)
    manage_hub.click_on_manage_roles()


@when(parsers.parse('I add a new role called "{role_name}" with permission to "{permissions}"'))
def add_a_role(driver, role_name, permissions, context):
    roles_page = RolesPages(driver)
    roles_page.click_add_a_role_button()
    if role_name == " ":
        context.role_name = role_name
    else:
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string)) - 14 :]
        context.role_name = role_name + extra_string

    roles_page.enter_role_name(context.role_name)
    roles_page.select_permissions(permissions)
    functions.click_submit(driver)


@then("I see the role in the roles list")
def see_role_in_list(driver, context):
    assert context.role_name in Shared(driver).get_text_of_govuk_table_body()


@when("I edit my role")
def edit_existing_role(driver, context):
    elements = Shared(driver).get_cells_in_gov_table()
    no = utils.get_element_index_by_text(elements, context.role_name)
    elements[no + 2].find_element_by_css_selector("a").click()
    roles_pages = RolesPages(driver)
    context.flag_name = str(context.role_name)[:12] + "edited"
    roles_pages.enter_role_name(context.role_name)
    functions.click_submit(driver)

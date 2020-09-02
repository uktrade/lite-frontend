from pytest_bdd import scenarios, when, parsers, then

from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.users_page import UsersPage
from ui_tests.caseworker.pages.roles_pages import RolesPages
import tests_common.tools.helpers as utils


scenarios("../features/roles.feature", strict_gherkin=False)


@when("I go to manage roles")
def go_to_manage_roles(driver):
    user_page = UsersPage(driver)
    user_page.click_on_manage_roles()


@when(
    parsers.parse(
        'I add a new role called "{role_name}" with permission to "{permissions}" and set status to "{status}"'
    )
)
def add_a_role(driver, role_name, permissions, status, context):
    roles_page = RolesPages(driver)
    roles_page.click_add_a_role_button()
    if role_name == " ":
        context.role_name = role_name
    else:
        context.role_name = f"{role_name} {utils.get_formatted_date_time_y_m_d_h_s()}"[:25]

    roles_page.enter_role_name(context.role_name)
    roles_page.select_permissions(permissions)
    roles_page.select_statuses(status)
    Shared(driver).click_submit()


@then("I see the role in the roles list")
def see_role_in_list(driver, context):
    assert context.role_name in Shared(driver).get_text_of_lite_table_body()


@when("I edit my role")
def edit_existing_role(driver, context):
    elements = Shared(driver).get_cells_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.role_name)
    elements[no + 2].find_element_by_css_selector("a").click()
    roles_pages = RolesPages(driver)
    context.flag_name = str(context.role_name)[:12] + "edited"
    roles_pages.enter_role_name(context.role_name)
    Shared(driver).click_submit()

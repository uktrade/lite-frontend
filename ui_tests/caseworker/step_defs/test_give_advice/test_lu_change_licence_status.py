from pytest_bdd import scenarios
from pytest_bdd import scenarios, when

from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.roles_pages import RolesPages
import tests_common.tools.helpers as utils

scenarios("../../features/give_advice/lu_licence_change_status.feature", strict_gherkin=False)


@when("I edit my role LU")
def edit_existing_role(driver, context):
    roles_page = RolesPages(driver)

    elements = Shared(driver).get_cells_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.role_name)
    elements[no + 2].find_element(by=By.CSS_SELECTOR, value="a").click()
    roles_pages = RolesPages(driver)
    context.flag_name = str(context.role_name)[:12] + "edited"
    roles_pages.enter_role_name(context.role_name)
    Shared(driver).click_submit()

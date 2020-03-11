from ui_automation_tests.shared.BasePage import BasePage


class RolesPages(BasePage):

    ADD_ROLE_TEXT_FIELD = "name"  # ID
    ADD_ROLE = "button-add-role"  # ID
    TAB_ROLES_ID = "tab-roles"

    def enter_role_name(self, text):
        self.driver.find_element_by_id(self.ADD_ROLE_TEXT_FIELD).clear()
        self.driver.find_element_by_id(self.ADD_ROLE_TEXT_FIELD).send_keys(text)

    def select_permissions(self, value):
        self.driver.find_element_by_id(value).click()

    def click_add_a_role_button(self):
        self.driver.find_element_by_id(self.ADD_ROLE).click()

    def click_on_manage_roles(self):
        self.driver.find_element_by_id(self.TAB_ROLES_ID).click()

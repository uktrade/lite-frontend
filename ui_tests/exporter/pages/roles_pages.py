from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.tools.helpers import find_paginated_item_by_id


class RolesPages(BasePage):

    ADD_ROLE_TEXT_FIELD = "name"  # ID
    ADD_ROLE = "button-add-role"  # ID
    TAB_ROLES_ID = "tab-roles"
    ROLE_PARTIAL_ID = "role-"
    EDIT_ROLE_PARTIAL_ID = "edit-"

    def enter_role_name(self, text):
        self.driver.find_element(by=By.ID, value=self.ADD_ROLE_TEXT_FIELD).clear()
        self.driver.find_element(by=By.ID, value=self.ADD_ROLE_TEXT_FIELD).send_keys(text)

    def select_permissions(self, value):
        self.driver.find_element(by=By.ID, value=value).click()

    def click_add_a_role_button(self):
        self.driver.find_element(by=By.ID, value=self.ADD_ROLE).click()

    def click_on_manage_roles(self):
        self.driver.find_element(by=By.ID, value=self.TAB_ROLES_ID).click()

    def click_edit_role(self, role_id):
        self.driver.find_element(by=By.ID, value=self.EDIT_ROLE_PARTIAL_ID + role_id).click()

    def find_role_row(self, role_id):
        return find_paginated_item_by_id(self.ROLE_PARTIAL_ID + role_id, self.driver)

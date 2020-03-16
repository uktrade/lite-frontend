from selenium.webdriver.support.ui import Select

from ui_automation_tests.shared.BasePage import BasePage
import ui_automation_tests.shared.tools.helpers as utils


class UsersPage(BasePage):
    BUTTON_ADD_USER_ID = "button-add-user"
    MANAGE_ROLES_BUTTON = "button-manage-roles"
    EMAIL = "email"
    TEAM = "team"
    ROLE = "role"
    LINK_CHANGE_EMAIL_ID = "link-edit-email"
    BUTTON_DEACTIVATE_USER_ID = "button-deactivate-user"
    BUTTON_REACTIVATE_USER_ID = "button-reactivate-user"
    DEACTIVATE_ARE_YOU_SURE_BUTTON_ID = "deactivated_button"
    REACTIVATE_ARE_YOU_SURE_BUTTON_ID = "reactivated_button"

    def click_add_a_user_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_USER_ID).click()

    def enter_email(self, email):
        self.driver.find_element_by_id(self.EMAIL).clear()
        self.driver.find_element_by_id(self.EMAIL).send_keys(email)

    def select_option_from_team_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.TEAM))
        select.select_by_visible_text(value)

    def select_option_from_role_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.ROLE))
        select.select_by_visible_text(value)

    def select_option_from_team_drop_down_by_value(self):
        select = Select(self.driver.find_element_by_id(self.TEAM))
        select.select_by_index(2)

    def click_on_manage_roles(self):
        self.driver.find_element_by_id(self.MANAGE_ROLES_BUTTON).click()

    def click_change_email_link(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_EMAIL_ID).click()

    def click_deactivate_user(self):
        self.driver.find_element_by_id(self.BUTTON_DEACTIVATE_USER_ID).click()
        self.driver.find_element_by_id(self.DEACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def click_reactivate_user(self):
        self.driver.find_element_by_id(self.BUTTON_REACTIVATE_USER_ID).click()
        self.driver.find_element_by_id(self.REACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def go_to_user_page(self, context):
        element_id = "link-" + context.added_email
        utils.find_paginated_item_by_id(element_id, self.driver)
        utils.scroll_to_element_by_id(self.driver, element_id)
        self.driver.find_element_by_id(element_id).click()

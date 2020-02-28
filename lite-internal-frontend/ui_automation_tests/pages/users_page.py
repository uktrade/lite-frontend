from selenium.webdriver.support.ui import Select

from ui_automation_tests.shared.BasePage import BasePage
import ui_automation_tests.shared.tools.helpers as utils


class UsersPage(BasePage):
    ADD_A_USER_BUTTON = "a[href*='/users/add']"
    SUBMIT_BUTTON = "button[type*='submit']"
    MANAGE_ROLES_BUTTON = "button-manage-roles"
    EMAIL = "email"
    TEAM = "team"
    ROLE = "role"
    EDIT_BUTTONS_IN_TABLE = '.govuk-table__cell a[href*="edit"]'
    EDIT_BUTTON_ON_USERS_PAGE = "edit_button"
    DEACTIVATE_BUTTON_CSS = '.govuk-button[href*="deactivate"]'
    REACTIVATE_BUTTON_CSS = '.govuk-button[href*="reactivate"]'
    DEACTIVATE_ARE_YOU_SURE_BUTTON_ID = "deactivated_button"
    REACTIVATE_ARE_YOU_SURE_BUTTON_ID = "reactivated_button"

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BUTTON).click()

    def click_add_a_user_btn(self):
        self.driver.find_element_by_css_selector(self.ADD_A_USER_BUTTON).click()

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

    def click_edit_button_by_index(self, index):
        self.driver.find_elements_by_css_selector(self.EDIT_BUTTONS_IN_TABLE)[index].click()

    def click_edit_button_on_users_page(self):
        self.driver.find_element_by_id(self.EDIT_BUTTON_ON_USERS_PAGE).click()

    def deactivate_user(self):
        self.driver.find_element_by_css_selector(self.DEACTIVATE_BUTTON_CSS).click()
        self.driver.find_element_by_id(self.DEACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def reactivate_user(self):
        self.driver.find_element_by_css_selector(self.REACTIVATE_BUTTON_CSS).click()
        self.driver.find_element_by_id(self.REACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def go_to_user_page(self, context):
        id = "edit-" + context.added_email
        utils.find_paginated_item_by_id(id, self.driver)
        self.driver.find_element_by_id(id).click()

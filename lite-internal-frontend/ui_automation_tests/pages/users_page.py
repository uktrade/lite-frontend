from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

from pages.shared import Shared
from shared import functions
from shared.BasePage import BasePage
import shared.tools.helpers as utils


class UsersPage(BasePage):
    ADD_A_USER_BUTTON = "a[href*='/users/add']"
    SUBMIT_BUTTON = "button[type*='submit']"
    PROFILE_LINK = "a[href*='/users/profile/']"
    MANAGE_ROLES_BUTTON = "button-manage-roles"
    EMAIL = "email"
    TEAM = "team"
    ROLE = "role"
    EDIT_BUTTONS_IN_TABLE = '.govuk-table__cell a[href*="edit"]'
    DEACTIVATE_BUTTON_CSS = '.govuk-button[href*="deactivate"]'
    REACTIVATE_BUTTON_CSS = '.govuk-button[href*="reactivate"]'
    DEACTIVATE_ARE_YOU_SURE_BUTTON_ID = "deactivated_button"
    REACTIVATE_ARE_YOU_SURE_BUTTON_ID = "reactivated_button"

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BUTTON).click()

    def click_add_a_user_btn(self):
        self.driver.find_element_by_css_selector(self.ADD_A_USER_BUTTON).click()

    def click_edit_for_user(self, user_name):
        element = self.driver.find_element_by_xpath(
            "//*[text()[contains(.,'" + user_name + "')]]/following-sibling::td[last()]/a"
        )
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        element.click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.PROFILE_LINK).click()

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

    def deactivate_user(self):
        self.driver.find_element_by_css_selector(self.DEACTIVATE_BUTTON_CSS).click()
        self.driver.find_element_by_id(self.DEACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def reactivate_user(self):
        self.driver.find_element_by_css_selector(self.REACTIVATE_BUTTON_CSS).click()
        self.driver.find_element_by_id(self.REACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def go_to_users_page(self, context):
        utils.find_paginated_item_by_id(context.added_email, self.driver)
        no = utils.get_element_index_by_text(
            Shared(self.driver).get_rows_in_lite_table(), context.added_email, complete_match=False
        )
        self.driver.find_elements_by_link_text("Edit")[no].click()
        functions.click_back_link(self.driver)

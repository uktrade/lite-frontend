from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time


class UsersPage:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit']"
        self.add_a_user_button = "a[href*='/users/add']"
        self.submit_button = "button[type*='submit']"
        self.first_name = "button[type*='submit']"
        self.last_name = "last_name"
        self.deactivate_button = ".govuk-button[href*='deactivate']"
        self.reactivate_button = ".govuk-button[href*='reactivate']"
        self.logout_button = "a[href*='/logout']"
        self.profile_link = "a[href*='/users/profile/']"
        self.manage_roles_button = "button-manage-roles"
        self.email = "email"
        self.team = "team"
        self.role = "role"
        self.edit_buttons_in_table = '.govuk-table__cell a[href*="edit"]'

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_add_a_user_btn(self):
        self.driver.find_element_by_css_selector(self.add_a_user_button).click()

    def enter_first_name(self, first_name):
        self.driver.find_element_by_id(self.first_name).clear()
        self.driver.find_element_by_id(self.first_name).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element_by_id(self.last_name).clear()
        self.driver.find_element_by_id(self.last_name).send_keys(last_name)

    def click_edit_for_user(self, user_name):
        element = self.driver.find_element_by_xpath(
            "//*[text()[contains(.,'" + user_name + "')]]/following-sibling::td[last()]/a")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        element.click()

    def click_user_name_link(self, user_name):
        element = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + user_name + "')]]")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        element.click()

    def click_deactivate_btn(self):
        self.driver.find_element_by_css_selector(self.deactivate_button).click()
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_reactivate_btn(self):
        self.driver.find_element_by_css_selector(self.reactivate_button).click()
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def logout(self):
        self.driver.find_element_by_css_selector(self.logout_button).click()
        assert "logout" in self.driver.current_url

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.profile_link).click()

    def enter_email(self, email):
        self.driver.find_element_by_id(self.email).clear()
        self.driver.find_element_by_id(self.email).send_keys(email)

    def select_option_from_team_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.team))
        select.select_by_visible_text(value)

    def select_option_from_role_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.role))
        select.select_by_visible_text(value)

    def select_option_from_team_drop_down_by_value(self):
        select = Select(self.driver.find_element_by_id(self.team))
        select.select_by_index(2)

    def click_on_manage_roles(self):
        self.driver.find_element_by_id(self.manage_roles_button).click()

    def click_edit_button_by_index(self, no):
        self.driver.find_elements_by_css_selector(self.edit_buttons_in_table)[no].click()

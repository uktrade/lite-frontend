from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time


class UsersPage:

    def __init__(self, driver):
        self.driver = driver

    def click_add_a_user_btn(self):
        self.driver.find_element_by_css_selector("a[href*='/users/add']").click()

    def enter_first_name(self, first_name):
        self.driver.find_element_by_id("first_name").clear()
        self.driver.find_element_by_id("first_name").send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element_by_id("last_name").clear()
        self.driver.find_element_by_id("last_name").send_keys(last_name)

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
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Deactivate')]]").click()
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Deactivate User')]]").click()

    def click_reactivate_btn(self):
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Reactivate')]]").click()
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Reactivate User')]]").click()

    def logout(self):
        self.driver.find_element_by_css_selector("a[href*='/logout']").click()
        assert "logout" in self.driver.current_url

    def click_user_profile(self):
        self.driver.find_element_by_css_selector("a[href*='/users/profile/']").click()

    def enter_email(self, email):
        self.driver.find_element_by_id("email").clear()
        self.driver.find_element_by_id("email").send_keys(email)

    def select_option_from_team_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id('team'))
        select.select_by_visible_text(value)

    def select_option_from_role_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id('role'))
        select.select_by_visible_text(value)

    def select_option_from_team_drop_down_by_value(self):
        select = Select(self.driver.find_element_by_id('team'))
        select.select_by_index(2)

    def click_on_manage_roles(self):
        self.driver.find_element_by_id("button-manage-roles").click()

from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class RolesPages(BasePage):

    ADD_ROLE_TEXT_FIELD = "name"  # ID
    ADD_ROLE = "button_add_role"  # ID

    def enter_role_name(self, text):
        self.driver.find_element(by=By.ID, value=self.ADD_ROLE_TEXT_FIELD).clear()
        self.driver.find_element(by=By.ID, value=self.ADD_ROLE_TEXT_FIELD).send_keys(text)

    def select_permissions(self, value):
        self.driver.find_element(by=By.ID, value=value.replace(" ", "-")).click()

    def click_add_a_role_button(self):
        self.driver.find_element(by=By.ID, value=self.ADD_ROLE).click()

    def select_statuses(self, value):
        self.driver.find_element(by=By.ID, value=value).click()

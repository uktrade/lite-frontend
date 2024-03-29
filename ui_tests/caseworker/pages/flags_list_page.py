from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage


class FlagsListPage(BasePage):
    BUTTON_ADD_FLAG_ID = "button-add-a-flag"
    CHECKBOX_ONLY_SHOW_DEACTIVATED_NAME = "status"

    def click_add_a_flag_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_ADD_FLAG_ID).click()

    def click_edit_link(self):
        self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Edit").click()

    def click_only_show_deactivated(self):
        functions.try_open_filters(self.driver)
        self.driver.find_element(by=By.NAME, value=self.CHECKBOX_ONLY_SHOW_DEACTIVATED_NAME).click()
        functions.click_apply_filters(self.driver)

    def click_deactivate_link(self):
        self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Deactivate").click()

    def click_reactivate_link(self):
        self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Reactivate").click()

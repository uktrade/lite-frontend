from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.exporter.pages.BasePage import BasePage


class StartPage(BasePage):
    BUTTON_SIGN_IN_ID = "button-sign-in"
    LINK_REGISTER_ID = "link-register"

    def try_click_sign_in_button(self):
        if functions.element_with_id_exists(self.driver, self.BUTTON_SIGN_IN_ID):
            self.driver.find_element(by=By.ID, value=self.BUTTON_SIGN_IN_ID).click()

    def click_register_link(self):
        self.driver.find_element_by_id(self.LINK_REGISTER_ID).click()

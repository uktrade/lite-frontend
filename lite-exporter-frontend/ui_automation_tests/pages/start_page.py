from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class StartPage(BasePage):
    BUTTON_SIGN_IN_ID = "button-sign-in"
    LINK_REGISTER_ID = "link-register"

    def try_click_sign_in_button(self):
        if functions.element_with_id_exists(self.driver, self.BUTTON_SIGN_IN_ID):
            self.driver.find_element_by_id(self.BUTTON_SIGN_IN_ID).click()

    def click_register_link(self):
        self.driver.find_element_by_id(self.LINK_REGISTER_ID).click()

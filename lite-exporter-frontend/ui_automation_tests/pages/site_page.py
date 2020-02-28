from ui_automation_tests.shared.BasePage import BasePage


class SitePage(BasePage):
    BUTTON_EDIT_ID = "button-edit"

    def click_edit_button(self):
        self.driver.find_element_by_id(self.BUTTON_EDIT_ID).click()

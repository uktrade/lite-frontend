from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class GenericApplicationUltimateEndUsers(BasePage):

    BUTTON_ADD_ULTIMATE_RECIPIENT_ID = "button-add-ultimate-recipient"
    TABLE_BODY = "tbody"
    TABLE_ROW = "tr"

    def get_ultimate_recipients(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_BODY + " " + self.TABLE_ROW)

    def click_add_ultimate_recipient_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_ADD_ULTIMATE_RECIPIENT_ID).click()

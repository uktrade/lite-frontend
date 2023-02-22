from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class ApplicationEditTypePage(BasePage):

    MAJOR_EDITS_RADIO_BUTTON = "edit-type-major"
    CHANGE_APPLICATION_BTN = '.govuk-button[value="submit"]'

    def click_major_edits_radio_button(self):
        self.driver.find_element(by=By.ID, value=self.MAJOR_EDITS_RADIO_BUTTON).click()

    def click_change_application_button(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.CHANGE_APPLICATION_BTN).click()

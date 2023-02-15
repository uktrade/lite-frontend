from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class WhichLocationFormPage(BasePage):
    RADIOBUTTON_LOCATION_ID_PREFIX = "choice-"

    def click_on_location_radiobutton(self, choice):
        self.driver.find_element(by=By.ID, value=self.RADIOBUTTON_LOCATION_ID_PREFIX + choice).click()

    def click_on_choice_radio_button(self, string):
        self.driver.find_element(by=By.ID, value="choice-" + string).click()

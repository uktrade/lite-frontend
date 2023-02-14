from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class LocationTypeFormPage(BasePage):
    RADIOBUTTON_LOCATION_ID_PREFIX = "location_type-"

    def click_on_location_type_radiobutton(self, location_type):
        self.driver.find_element(by=By.ID, value=self.RADIOBUTTON_LOCATION_ID_PREFIX + location_type).click()

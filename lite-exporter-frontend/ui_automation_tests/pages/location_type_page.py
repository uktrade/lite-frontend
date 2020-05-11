from ui_automation_tests.shared.BasePage import BasePage


class LocationTypeFormPage(BasePage):
    RADIOBUTTON_LOCATION_ID_PREFIX = "location_type-"

    def click_on_location_type_radiobutton(self, location_type):
        self.driver.find_element_by_id(self.RADIOBUTTON_LOCATION_ID_PREFIX + location_type).click()

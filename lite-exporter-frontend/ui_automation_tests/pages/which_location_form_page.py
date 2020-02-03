from shared.BasePage import BasePage


class WhichLocationFormPage(BasePage):
    RADIOBUTTON_LOCATION_ID_PREFIX = "choice-"

    def click_on_location_radiobutton(self, choice):
        self.driver.find_element_by_id(self.RADIOBUTTON_LOCATION_ID_PREFIX + choice).click()

    def click_on_choice_radio_button(self, string):
        self.driver.find_element_by_id("choice-" + string).click()

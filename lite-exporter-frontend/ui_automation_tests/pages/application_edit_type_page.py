from shared.BasePage import BasePage


class ApplicationEditTypePage(BasePage):

    MINOR_EDITS_RADIO_BUTTON = "edit-type-minor"
    MAJOR_EDITS_RADIO_BUTTON = "edit-type-major"
    CHANGE_APPLICATION_BTN = '.govuk-button[value="submit"]'

    def click_minor_edits_radio_button(self):
        self.driver.find_element_by_id(self.MINOR_EDITS_RADIO_BUTTON).click()

    def click_major_edits_radio_button(self):
        self.driver.find_element_by_id(self.MAJOR_EDITS_RADIO_BUTTON).click()

    def click_change_application_button(self):
        self.driver.find_element_by_css_selector(self.CHANGE_APPLICATION_BTN).click()

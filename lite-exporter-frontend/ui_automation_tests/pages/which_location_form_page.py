from shared.BasePage import BasePage


class WhichLocationFormPage(BasePage):
    ORGANISATION_OR_EXTERNAL_RADIO_BUTTON = "organisation_or_external-"

    def click_on_organisation_or_external_radio_button(self, string):
        self.driver.find_element_by_id(self.ORGANISATION_OR_EXTERNAL_RADIO_BUTTON + string).click()

    def click_on_choice_radio_button(self, string):
        self.driver.find_element_by_id("choice-" + string).click()

class WhichLocationFormPage:

    def __init__(self, driver):
        self.driver = driver
        self.organisation_or_external_radio_button = "organisation_or_external-"

    def click_on_organisation_or_external_radio_button(self, string):
        self.driver.find_element_by_id(self.organisation_or_external_radio_button + string).click()

    def click_on_choice_radio_button(self, string):
        self.driver.find_element_by_id('choice-' + string).click()

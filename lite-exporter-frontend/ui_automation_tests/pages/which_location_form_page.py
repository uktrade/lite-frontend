class WhichLocationFormPage:

    def __init__(self, driver):
        self.driver = driver
        self.organisation_or_external_radio_button = "organisation_or_external-"
        self.submit_button = "button[type*='submit']"

    def click_on_organisation_or_external_radio_button(self, string):
        self.driver.find_element_by_id(self.organisation_or_external_radio_button + string).click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_continue(self):
        self.click_save_and_continue()

class ApplicationEditTypePage:

    def __init__(self, driver):
        self.driver = driver
        self.minor_edits_radio_button = "edit-type-minor"
        self.major_edits_radio_button = "edit-type-major"
        self.change_application_btn = '.govuk-button[type="submit"][value="submit"]'

    def click_minor_edits_radio_button(self):
        self.driver.find_element_by_id(self.minor_edits_radio_button).click()

    def click_major_edits_radio_button(self):
        self.driver.find_element_by_id(self.major_edits_radio_button).click()

    def click_change_application_button(self):
        self.driver.find_element_by_css_selector(self.change_application_btn).click()


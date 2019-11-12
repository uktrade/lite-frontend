class PreexistingLocationsPage:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit'][value='submit']"
        self.external_locations_checkbox = ".govuk-checkboxes__input"

    def click_external_locations_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.external_locations_checkbox)[no].click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_continue(self):
        self.click_save_and_continue()

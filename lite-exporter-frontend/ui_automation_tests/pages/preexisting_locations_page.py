class PreexistingLocationsPage:

    def __init__(self, driver):
        self.driver = driver
        self.external_locations_checkbox = ".govuk-checkboxes__input"

    def click_external_locations_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.external_locations_checkbox)[no].click()

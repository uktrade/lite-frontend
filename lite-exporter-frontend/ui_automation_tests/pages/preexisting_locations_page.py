from shared.BasePage import BasePage


class PreexistingLocationsPage(BasePage):
    EXTERNAL_LOCATIONS_CHECKBOX = ".govuk-checkboxes__input"

    def click_external_locations_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.EXTERNAL_LOCATIONS_CHECKBOX)[no].click()

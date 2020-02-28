from ui_automation_tests.shared.BasePage import BasePage


class SitesPage(BasePage):
    SITES_CHECKBOX = ".govuk-checkboxes__input"

    def click_sites_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.SITES_CHECKBOX)[no].click()

    def get_checked_attribute_of_sites_checkbox(self, no):
        return self.driver.find_elements_by_css_selector(self.SITES_CHECKBOX)[no].get_attribute("checked")

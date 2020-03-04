from ui_automation_tests.shared.BasePage import BasePage


class SitesPage(BasePage):
    SITES_CHECKBOX = ".govuk-checkboxes__input"

    def click_sites_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.SITES_CHECKBOX)[no].click()

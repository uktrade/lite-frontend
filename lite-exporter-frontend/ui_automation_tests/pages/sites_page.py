from shared.BasePage import BasePage


class SitesPage(BasePage):
    SITES_CHECKBOX = ".govuk-checkboxes__input"
    SITES_LABEL = ".govuk-checkboxes__label"

    def click_sites_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.SITES_CHECKBOX)[no].click()

    def get_checked_attribute_of_sites_checkbox(self, no):
        return self.driver.find_elements_by_css_selector(self.SITES_CHECKBOX)[no].get_attribute("checked")

    def get_text_of_site(self, no):
        return self.driver.find_elements_by_css_selector(self.SITES_LABEL)[no].text

    def get_size_of_sites(self):
        return len(self.driver.find_elements_by_css_selector(self.SITES_LABEL))

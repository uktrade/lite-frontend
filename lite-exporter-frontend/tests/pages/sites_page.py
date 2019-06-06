class SitesPage():

    def __init__(self, driver):
        self.driver = driver
        self.sites_checkbox = ".govuk-checkboxes__input"
        self.sites_label = ".govuk-checkboxes__input"

    def click_sites_checkbox(self, no):
        self.driver.find_elements_by_css_selector(self.sites_checkbox)[no].click()

    def get_checked_attribute_of_sites_checkbox(self, no):
        return self.driver.find_elements_by_css_selector(self.sites_checkbox)[no].get_attribute("checked")

    def get_text_of_site(self, no):
        return self.driver.find_elements_by_css_selector(".govuk-checkboxes__label")[no].text

    def get_size_of_sites(self):
        return len(self.driver.find_elements_by_css_selector(".govuk-checkboxes__label"))


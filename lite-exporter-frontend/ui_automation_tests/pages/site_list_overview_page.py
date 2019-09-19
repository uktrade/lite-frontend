class SitesListOverview:

    def __init__(self, driver):
        self.driver = driver
        self.new_sites_link = ".govuk-button[href*='new']"
        self.edit_buttons = ".govuk-table__cell .govuk-link"
        self.table_cells = ".govuk-table__cell"

    def click_new_sites_link(self):
        self.driver.find_element_by_css_selector(self.new_sites_link).click()

    def click_on_the_edit_button_at_last_position(self):
        self.driver.find_elements_by_css_selector(self.edit_buttons)[len(self.driver.find_elements_by_css_selector(self.edit_buttons))-1].click()

    def get_text_of_last_site_name(self):
        return self.driver.find_elements_by_css_selector(self.table_cells)[len(self.driver.find_elements_by_css_selector(self.table_cells))-3].text


class SitesListOverview():

    def __init__(self, driver):
        self.driver = driver
        self.new_sites_link = self.driver.find_element_by_css_selector(".govuk-button[href*='new']")
        self.edit_buttons = self.driver.find_elements_by_css_selector(".lite-table__cell .govuk-link")
        self.table_cells = self.driver.find_elements_by_css_selector(".lite-table__cell")


    def click_new_sites_link(self):
        self.new_sites_link.click()

    def click_on_the_edit_button_at_last_position(self):
        self.edit_buttons[len(self.edit_buttons)-1].click()

    def get_text_of_last_site_name(self):
        return self.table_cells[len(self.table_cells)-3].text


from shared.BasePage import BasePage


class SitesListOverview(BasePage):
    NEW_SITES_LINK = ".govuk-button[href*='new']"
    EDIT_BUTTONS = ".govuk-table__cell .govuk-link"
    TABLE_CELLS = ".govuk-table__cell"

    def click_new_sites_link(self):
        self.driver.find_element_by_css_selector(self.NEW_SITES_LINK).click()

    def click_on_the_edit_button_at_first_position(self):
        self.driver.find_elements_by_css_selector(self.EDIT_BUTTONS)[0].click()

    def get_text_of_first_site_name(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_CELLS)[0].text

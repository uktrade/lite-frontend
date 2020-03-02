from ui_automation_tests.shared.BasePage import BasePage


class SitesListOverview(BasePage):
    BUTTON_NEW_SITE_ID = "button-add-site"
    VIEW_LINKS_SELECTOR = ".govuk-table__cell .govuk-link"

    def click_new_site_link(self):
        self.driver.find_element_by_id(self.BUTTON_NEW_SITE_ID).click()

    def click_on_the_view_button_at_first_position(self):
        self.driver.find_elements_by_css_selector(self.VIEW_LINKS_SELECTOR)[0].click()

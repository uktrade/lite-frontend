from ui_automation_tests.shared.BasePage import BasePage


class GoodsLocationsPage(BasePage):

    EDIT_SITES_BUTTON = 'a[href*="existing-sites"]'

    def click_edit_sites_button(self):
        self.driver.find_element_by_css_selector(self.EDIT_SITES_BUTTON).click()

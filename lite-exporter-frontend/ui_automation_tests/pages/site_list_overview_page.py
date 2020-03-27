from ui_automation_tests.shared.BasePage import BasePage


class SitesListOverview(BasePage):
    BUTTON_NEW_SITE_ID = "button-add-site"

    def click_new_site_link(self):
        self.driver.find_element_by_id(self.BUTTON_NEW_SITE_ID).click()

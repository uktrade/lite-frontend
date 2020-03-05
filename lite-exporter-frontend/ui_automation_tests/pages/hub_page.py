from ui_automation_tests.shared.BasePage import BasePage


class Hub(BasePage):

    SWITCH_LINK = "switch-link"  # ID
    SITES_BTN = "[href*='/sites/']"  # CSS
    APPLICATION_BTN = "a[href*='/applications/']"  # CSS
    APPLICATIONS_TILE = '.app-tiles [href="/applications/"] p'  # ID

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.APPLICATION_BTN).click()

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.SITES_BTN).click()

    def click_switch_link(self):
        self.driver.find_element_by_id(self.SWITCH_LINK).click()

    def get_text_of_application_tile(self):
        return self.driver.find_element_by_css_selector(self.APPLICATIONS_TILE).text

    def return_number_of_notifications(self):
        text_of_new_notifications = self.driver.find_element_by_css_selector(self.APPLICATIONS_TILE).text
        if "You have" in text_of_new_notifications:
            total_of_notifications = int((text_of_new_notifications.split("have "))[1].split(" new")[0])
        else:
            total_of_notifications = 0
        return total_of_notifications

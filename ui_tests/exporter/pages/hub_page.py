from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class Hub(BasePage):

    SWITCH_LINK = "switch-link"  # ID
    SITES_BTN = "[href*='/sites/']"  # CSS
    APPLICATION_BTN = "a[href*='/applications/']"  # CSS
    TILE_APPLICATIONS_ID = "applications-notifications"  # ID

    def click_applications(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.APPLICATION_BTN).click()

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.SITES_BTN).click()

    def click_switch_link(self):
        self.driver.find_element_by_id(self.SWITCH_LINK).click()

    def get_text_of_application_tile(self):
        return self.driver.find_element_by_id(self.TILE_APPLICATIONS_ID).text

    def return_number_of_notifications(self):
        text_of_new_notifications = self.driver.find_element_by_id(self.TILE_APPLICATIONS_ID).text
        # Returns (n notifications) so filter just to return the digits
        return int("".join(filter(str.isdigit, text_of_new_notifications)))

    def notification_bubble_exists(self):
        notification_exists = self.driver.find_element(by=By.ID, value=self.TILE_APPLICATIONS_ID).is_displayed()
        return notification_exists

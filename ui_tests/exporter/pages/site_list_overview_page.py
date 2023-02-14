from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class SitesListOverview(BasePage):
    BUTTON_NEW_SITE_ID = "button-add-site"

    def click_new_site_link(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_NEW_SITE_ID).click()

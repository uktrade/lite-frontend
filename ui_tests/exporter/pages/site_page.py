from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class SitePage(BasePage):
    LINK_CHANGE_NAME_ID = "link-change-name"

    def click_change_name_link(self):
        self.driver.find_element(by=By.ID, value=self.LINK_CHANGE_NAME_ID).click()

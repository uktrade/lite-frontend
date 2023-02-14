from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class ExhibitionClearanceGoodPage(BasePage):
    GOOD_TYPE_PARTIAL_ID = "item_type-"

    def click_good_type(self, type):
        self.driver.find_element(by=By.ID, value=self.GOOD_TYPE_PARTIAL_ID + type).click()

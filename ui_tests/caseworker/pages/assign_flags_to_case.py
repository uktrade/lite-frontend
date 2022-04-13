from selenium.webdriver.common.by import By
from tests_common import selectors
from ui_tests.caseworker.pages.BasePage import BasePage


class CaseFlagsPages(BasePage):
    def select_flag(self, flag_name):
        self.driver.find_element(by=By.ID, value="filter-box").send_keys(flag_name)
        if (
            not self.driver.find_element(
                by=By.CSS_SELECTOR, value=selectors.VISIBLE + " " + selectors.CHECKBOX
            ).get_attribute("checked")
            == "true"
        ):
            self.driver.find_element(by=By.CSS_SELECTOR, value=selectors.VISIBLE + " " + selectors.CHECKBOX).click()

    def deselect_flag(self, flag_name):
        self.driver.find_element_by_id("filter-box").send_keys(flag_name)
        if (
            self.driver.find_element(
                by=By.CSS_SELECTOR, value=selectors.VISIBLE + " " + selectors.CHECKBOX
            ).get_attribute("checked")
            == "true"
        ):
            self.driver.find_element(by=By.CSS_SELECTOR, value=selectors.VISIBLE + " " + selectors.CHECKBOX).click()

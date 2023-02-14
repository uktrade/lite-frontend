from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_by_id


class RecordDecision(BasePage):
    def click_on_decision_number(self, no):
        scroll_to_element_by_id(self.driver, no)
        self.driver.find_element(by=By.ID, value=no).click()

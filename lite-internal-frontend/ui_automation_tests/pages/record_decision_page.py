from pages.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id


class RecordDecision(BasePage):
    def click_on_decision_number(self, no):
        scroll_to_element_by_id(self.driver, no)
        self.driver.find_element_by_id(no).click()

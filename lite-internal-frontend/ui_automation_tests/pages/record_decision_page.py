from shared.BasePage import BasePage


class RecordDecision(BasePage):
    def click_on_decision_number(self, no):
        self.driver.find_element_by_id(no).click()

from pages.BasePage import BasePage
from shared import selectors


class UnassignQueuePage(BasePage):
    def check_all_checkboxes(self):
        for checkbox in self.driver.find_elements_by_css_selector(selectors.CHECKBOX):
            checkbox.click()

    def check_unassign_checkbox(self, queue_name):
        self.driver.find_element_by_id(queue_name).click()

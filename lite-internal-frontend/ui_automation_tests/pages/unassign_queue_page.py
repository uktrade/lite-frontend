from pages.BasePage import BasePage


class UnassignQueuePage(BasePage):
    def check_unassign_checkbox(self, queue_name):
        self.driver.find_element_by_id(queue_name).click()

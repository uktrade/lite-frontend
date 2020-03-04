from selenium.common.exceptions import NoSuchElementException

from ui_automation_tests.shared.BasePage import BasePage
from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id


class TaskListPage(BasePage):
    STATUS_PARTIAL_ID = "-status"
    TASK_LIST_ITEMS_CSS = ".lite-task-list__items"
    REMOVE_PARTY_LINK = "a[href*='remove']"

    def click_on_task_list_section(self, section):
        scroll_to_element_by_id(self.driver, section)
        self.driver.find_element_by_id(section).click()

    def get_section_status(self, section):
        return self.driver.find_element_by_id(section + self.STATUS_PARTIAL_ID).get_attribute("data-status")

    def get_text_of_lite_task_list_items(self):
        return self.driver.find_element_by_css_selector(self.TASK_LIST_ITEMS_CSS).text

    def find_remove_party_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_PARTY_LINK)
        except NoSuchElementException:
            return None

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_by_id


class TaskListPage(BasePage):
    STATUS_PARTIAL_ID = "-status"
    TASK_LIST_ITEMS_CSS = ".lite-task-list__items"
    REMOVE_PARTY_LINK = "a[href*='remove']"

    def click_on_task_list_section(self, section):
        scroll_to_element_by_id(self.driver, section)
        self.driver.find_element(by=By.ID, value=section).click()

    def get_section_status(self, section):
        return self.driver.find_element_by_id(section + self.STATUS_PARTIAL_ID).get_attribute("data-status")

    def get_section(self, section):
        section = self.driver.find_elements_by_id(section)
        return section[0] if section else None

    def get_text_of_lite_task_list_items(self):
        return self.driver.find_element_by_css_selector(self.TASK_LIST_ITEMS_CSS).text

    def find_remove_party_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_PARTY_LINK)
        except NoSuchElementException:
            return None

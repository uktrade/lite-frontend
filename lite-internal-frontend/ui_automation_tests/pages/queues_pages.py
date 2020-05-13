from selenium.webdriver.support.select import Select

from shared import functions
from shared.BasePage import BasePage


class QueuesPages(BasePage):
    ADD_QUEUE_TEXT_FIELD = "name"  # ID
    ADD_QUEUE_BUTTON = ".govuk-button[href*='queues/add']"  # CSS
    NO_CASES_TEXT = ".lite-information-text__text"  # CSS
    QUEUE_CHECKBOXES = ".govuk-checkboxes .govuk-checkboxes__input"  # CSS
    TABLE_ROWS = ".govuk-table__body .govuk-table__row"  # CSS
    LINK_EDIT_SELECTOR = '.govuk-link[href*="edit"]'
    SELECT_COUNTERSIGNING_QUEUE_ID = "countersigning_queue"

    def enter_queue_name(self, text):
        self.driver.find_element_by_id(self.ADD_QUEUE_TEXT_FIELD).clear()
        self.driver.find_element_by_id(self.ADD_QUEUE_TEXT_FIELD).send_keys(text)

    def click_add_a_queue_button(self):
        self.driver.find_element_by_css_selector(self.ADD_QUEUE_BUTTON).click()

    def is_case_on_the_list(self, app_id):
        no = len(self.driver.find_elements_by_css_selector('[href*="' + app_id + '"]'))
        while no == 0:
            functions.click_next_page(self.driver)
            no = len(self.driver.find_elements_by_css_selector("[href*='" + app_id + "']"))
        return no

    def is_no_cases_notice_displayed(self):
        return self.driver.find_element_by_css_selector(self.NO_CASES_TEXT).is_displayed()

    def click_queue_edit_button(self, num):
        self.driver.find_elements_by_css_selector(self.TABLE_ROWS)[num].find_element_by_css_selector(
            self.LINK_EDIT_SELECTOR
        ).click()

    def get_number_of_selected_queues(self):
        no = 0
        elements = self.driver.find_elements_by_css_selector(self.QUEUE_CHECKBOXES)
        for element in elements:
            if element.is_selected():
                no += 1
        return no

    def get_row_text(self, id):
        return self.driver.find_element_by_id(id).text

    def select_countersigning_queue(self, queue_name):
        Select(self.driver.find_element_by_id(self.SELECT_COUNTERSIGNING_QUEUE_ID)).select_by_visible_text(queue_name)

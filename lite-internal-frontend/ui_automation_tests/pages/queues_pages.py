from helpers.BasePage import BasePage


class QueuesPages(BasePage):
    ADD_QUEUE_TEXT_FIELD = "name"  # ID
    ADD_QUEUE_BUTTON = ".govuk-button[href*='queues/add']"  # CSS
    NO_CASES_TEXT = ".lite-information-text__text"  # CSS
    QUEUE_CHECKBOXES = ".govuk-checkboxes .govuk-checkboxes__input"  # CSS
    TABLE_ROWS = ".govuk-table__body .govuk-table__row"  # CSS
    QUEUES_EDIT_LINK = '.govuk-link[href*="queues"]'

    def enter_queue_name(self, text):
        self.driver.find_element_by_id(self.ADD_QUEUE_TEXT_FIELD).clear()
        self.driver.find_element_by_id(self.ADD_QUEUE_TEXT_FIELD).send_keys(text)

    def click_add_a_queue_button(self):
        self.driver.find_element_by_css_selector(self.ADD_QUEUE_BUTTON).click()

    def is_case_on_the_list(self, app_id):
        self.driver.set_timeout_to(0)
        no = len(self.driver.find_elements_by_css_selector('[href*="' + app_id + '"]'))
        url = self.driver.current_url
        page_number = 1
        while no == 0:
            page_number += 1
            next_page = url

            if "queue_id" not in url:
                next_page = url + "?queue_id=00000000-0000-0000-0000-000000000001"

            next_page = next_page + "&page=" + str(page_number)

            self.driver.get(next_page)
            no = len(self.driver.find_elements_by_css_selector("[href*='" + app_id + "']"))
        return no

    def get_no_cases_text(self):
        return self.driver.find_element_by_css_selector(self.NO_CASES_TEXT).text

    def click_queue_edit_button(self, num):
        self.driver.find_elements_by_css_selector(self.TABLE_ROWS)[num].find_element_by_css_selector(
            self.QUEUES_EDIT_LINK
        ).click()

    def deselect_all_queues(self):
        elements = self.driver.find_elements_by_css_selector(self.QUEUE_CHECKBOXES)
        for element in elements:
            if element.is_selected():
                element.click()

    def get_size_of_selected_queues(self):
        no = 0
        elements = self.driver.find_elements_by_css_selector(self.QUEUE_CHECKBOXES)
        for element in elements:
            if element.is_selected():
                no += 1
        return no

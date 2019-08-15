class QueuesPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_queue_text_field = "name"  # ID
        self.add_queue_button = ".govuk-button[href*='queues/add']"  # CSS
        self.no_cases_text = '.lite-information-text__text'  # CSS
        self.new_cases_queue = "New Cases"  # ID
        self.queue_checkboxes = ".govuk-checkboxes .govuk-checkboxes__input"  # CSS
        self.table_rows = ".govuk-table__body .govuk-table__row"
        self.queues_edit_link = '.govuk-table__body .govuk-link[href*="queues"]'

    def enter_queue_name(self, text):
        self.driver.find_element_by_id(self.add_queue_text_field).clear()
        self.driver.find_element_by_id(self.add_queue_text_field).send_keys(text)

    def click_add_a_queue_button(self):
        self.driver.find_element_by_css_selector(self.add_queue_button).click()

    def is_case_on_the_list(self, app_id):
        self.driver.set_timeout_to(0)
        no = len(self.driver.find_elements_by_link_text(app_id))
        self.driver.set_timeout_to_10_seconds()

        return no

    def get_no_cases_text(self):
        return self.driver.find_element_by_css_selector(self.no_cases_text).text

    def get_table_rows(self):
        return self.driver.find_elements_by_css_selector(self.table_rows)

    def click_queue_edit_button(self, num):
        self.driver.find_elements_by_css_selector(self.table_rows)[num].find_element_by_css_selector(self.queues_edit_link).click()

    def click_on_new_cases_queue(self):
        self.driver.find_element_by_id(self.new_cases_queue).click()

    def deselect_all_queues(self):
        elements = self.driver.find_elements_by_css_selector(self.queue_checkboxes)
        for element in elements:
            if element.is_selected():
                element.click()

    def get_size_of_selected_queues(self):
        no = 0
        elements = self.driver.find_elements_by_css_selector(self.queue_checkboxes)
        for element in elements:
            if element.is_selected():
                no += 1
        return no

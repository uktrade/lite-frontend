from shared.BasePage import BasePage


class ClcQueriesPages(BasePage):

    CONTROL_RESPONSE = "is_good_controlled-"  # ID
    CONTROL_LIST_ENTRY = "control_code"  # ID
    REPORT_SUMMARY = "report_summary"  # Name
    COMMENT = "comment"  # ID
    CASE_CLOSE = ".lite-info-bar"  # CSS
    RESPOND_BTN = "respond"  # ID
    SUBMIT_BUTTON = '.govuk-button[type*="submit"]'  # CSS

    def click_respond_to_query(self):
        self.driver.find_element_by_id(self.RESPOND_BTN).click()

    # Response Page
    def click_is_good_controlled(self, answer):
        self.driver.find_element_by_id(self.CONTROL_RESPONSE + answer).click()

    def type_in_to_control_list_entry(self, code):
        self.driver.find_element_by_id(self.CONTROL_LIST_ENTRY).clear()
        self.driver.find_element_by_id(self.CONTROL_LIST_ENTRY).send_keys(code)

    def choose_report_summary(self, num):
        element = self.driver.find_elements_by_name(self.REPORT_SUMMARY)[int(num)]
        self.driver.execute_script("arguments[0].click();", element)

    def enter_a_comment(self, comment):
        self.driver.find_element_by_id(self.COMMENT).send_keys(comment)

    def is_clc_query_case_closed(self):
        return len(self.driver.find_elements_by_css_selector(self.CASE_CLOSE)) == 1

    def is_respond_to_query_button_present(self):
        return len(self.driver.find_elements_by_id(self.RESPOND_BTN)) == 1

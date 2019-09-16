from helpers.BasePage import BasePage


class ClcQueriesPages(BasePage):

    respond_to_query_btn = '.govuk-button[href*="respond-to-query"]'  # css
    control_response = 'is_good_controlled-'  # id
    control_code = 'control_code'
    report_summary = 'report_summary'  # name
    comment = 'comment'  # id
    case_close = '.lite-info-bar'  # css
    submit_button = '.govuk-button[type*="submit"]'

    def click_respond_to_query(self):
        self.driver.find_element_by_css_selector(self.respond_to_query_btn).click()

    # Response Page
    def click_is_good_controlled(self, answer):
        self.driver.find_element_by_id(self.control_response + answer).click()

    def type_in_to_control_list_entry(self, code):
        self.driver.find_element_by_id(self.control_code).send_keys(code)

    def choose_report_summary(self, num):
        self.driver.find_elements_by_name(self.report_summary)[int(num)].click()

    def enter_a_comment(self, comment):
        self.driver.find_element_by_id(self.comment).send_keys(comment)

    def is_clc_query_case_closed(self):
        return len(self.driver.find_elements_by_css_selector(self.case_close)) == 1

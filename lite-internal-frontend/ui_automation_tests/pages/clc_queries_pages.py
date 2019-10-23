from helpers.BasePage import BasePage


class ClcQueriesPages(BasePage):

    respond_to_query_btn = '.govuk-button[href*="respond-to-query"]'  # css
    control_response = 'is_good_controlled-'  # id
    control_list_entry = 'control_code'
    report_summary = 'report_summary'  # name
    comment = 'comment'  # id
    case_close = '.lite-info-bar'  # css
    app_bar = '.lite-app-bar'  # css
    submit_button = '.govuk-button[type*="submit"]'

    def click_respond_to_query(self):
        self.driver.find_element_by_css_selector(self.respond_to_query_btn).click()

    # Response Page
    def click_is_good_controlled(self, answer):
        self.driver.find_element_by_id(self.control_response + answer).click()

    def type_in_to_control_list_entry(self, code):
        self.driver.find_element_by_id(self.control_list_entry).clear()
        self.driver.find_element_by_id(self.control_list_entry).send_keys(code)

    def choose_report_summary(self, num):
        element = self.driver.find_elements_by_name(self.report_summary)[int(num)]
        self.driver.execute_script('arguments[0].click();', element)

    def enter_a_comment(self, comment):
        self.driver.find_element_by_id(self.comment).send_keys(comment)

    def is_clc_query_case_closed(self):
        return len(self.driver.find_elements_by_css_selector(self.case_close)) == 1

    def is_respond_to_query_button_present(self):
        return "Respond to query" in self.driver.find_element_by_css_selector(self.app_bar).text

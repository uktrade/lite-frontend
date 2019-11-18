from shared.BasePage import BasePage


class ApplicationPage(BasePage):
    BUTTON_WITHDRAW_APPLICATION_ID = "button-withdraw-application"
    BUTTON_EDIT_APPLICATION_ID = "button-edit-application"
    LABEL_APPLICATION_STATUS_ID = "label-application-status"
    ECJU_QUERY_TAB = "ecju-queries-tab"  # ID
    ECJU_QUERY_RESPONSE_TEXT = "Respond to query"  # text
    ECJU_QUERIES_CLOSED = "closed-ecju-query"  # ID
    LINK_EDIT_APPLICATION = "a[href*='/edit-type/']"

    def click_withdraw_application_button(self):
        self.driver.find_element_by_id(self.BUTTON_WITHDRAW_APPLICATION_ID).click()

    def click_edit_application_link(self):
        self.driver.find_element_by_css_selector(self.LINK_EDIT_APPLICATION).click()

    def click_ecju_query_tab(self):
        self.driver.find_element_by_id(self.ECJU_QUERY_TAB).click()

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ECJU_QUERIES_CLOSED))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ECJU_QUERY_RESPONSE_TEXT + '")]'
        self.driver.find_elements_by_xpath(response)[no].click()

    def find_edit_application_button(self):
        return self.driver.find_elements_by_id(self.BUTTON_EDIT_APPLICATION_ID)

    def get_status(self):
        return self.driver.find_element_by_id(self.LABEL_APPLICATION_STATUS_ID).text

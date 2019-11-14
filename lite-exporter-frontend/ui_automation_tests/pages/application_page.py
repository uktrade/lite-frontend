class ApplicationPage:

    def __init__(self, driver):
        self.driver = driver
        self.ecju_query_tab = "ecju-queries-tab"  # ID
        self.ecju_query_response_text = 'Respond to query'  # text
        self.ecju_queries_closed = "closed-ecju-query"  # ID
        self.edit_application_link = "a[href*='/edit-type/']"
        self.edit_application_button = "edit-application-button"  # ID

    def click_edit_application_link(self):
        self.driver.find_element_by_css_selector(self.edit_application_link).click()

    def click_ecju_query_tab(self):
        self.driver.find_element_by_id(self.ecju_query_tab).click()

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ecju_queries_closed))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ecju_query_response_text + '")]'
        self.driver.find_elements_by_xpath(response)[no].click()

    def find_edit_application_button(self):
        return self.driver.find_elements_by_id(self.edit_application_button)

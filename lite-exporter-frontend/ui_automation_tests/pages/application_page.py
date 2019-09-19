class ApplicationPage:

    def __init__(self, driver):
        self.driver = driver
        self.ecju_query_tab = "ecju-queries-tab"  # ID
        self.ecju_query_response_text = 'Respond to query'  # text
        self.ecju_queries_closed = "closed-ecju-query"  # ID

    def click_ecju_query_tab(self):
        self.driver.find_element_by_id(self.ecju_query_tab).click()

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ecju_queries_closed))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ecju_query_response_text + '")]'
        self.driver.find_elements_by_xpath(response)[no].click()

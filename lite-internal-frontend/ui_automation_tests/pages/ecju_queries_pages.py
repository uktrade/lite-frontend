from shared.BasePage import BasePage


class EcjuQueriesPages(BasePage):
    BUTTON_NEW_QUERY_ID = "button-new-query"
    TEXTAREA_QUESTION_ID = "question"
    OPEN_QUERIES_ID = "open-queries"
    CLOSED_QUERIES_ID = "closed-queries"

    def enter_question_text(self, text):
        self.driver.find_element_by_id(self.TEXTAREA_QUESTION_ID).send_keys(text)

    def click_new_query_button(self):
        self.driver.find_element_by_id(self.BUTTON_NEW_QUERY_ID).click()

    def get_open_queries_text(self):
        return self.driver.find_element_by_id(self.OPEN_QUERIES_ID).text

    def get_closed_queries_text(self):
        return self.driver.find_element_by_id(self.CLOSED_QUERIES_ID).text

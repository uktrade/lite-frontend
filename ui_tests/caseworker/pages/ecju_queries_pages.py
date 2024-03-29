from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class EcjuQueriesPages(BasePage):
    BUTTON_NEW_QUERY_ID = "button-new-query"
    BUTTON_PREVISIT_QUESTIONNAIRE_ID = "button-new-pre-visit-questionnaire"
    BUTTON_COMPLIANCE_ACTIONS_ID = "button-new-compliance-actions"
    TEXTAREA_QUESTION_ID = "question"
    OPEN_QUERIES_ID = "open-queries"
    CLOSED_QUERIES_ID = "closed-queries"

    def enter_question_text(self, text):
        self.driver.find_element(by=By.ID, value=self.TEXTAREA_QUESTION_ID).send_keys(text)

    def enter_response_and_submit(self, response_text):
        open_queries = self.driver.find_element(by=By.ID, value="open-queries")
        element = open_queries.find_element(by=By.CLASS_NAME, value="govuk-textarea")
        element.clear()
        element.send_keys(response_text)

        # submit response
        submit = open_queries.find_element(by=By.ID, value="id_submit")
        submit.click()

    def click_new_query_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_NEW_QUERY_ID).click()

    def get_open_queries_text(self):
        return self.driver.find_element(by=By.ID, value=self.OPEN_QUERIES_ID).text

    def get_closed_queries_text(self):
        return self.driver.find_element(by=By.ID, value=self.CLOSED_QUERIES_ID).text

    def new_query_button_visible(self):
        return self.driver.find_element(by=By.ID, value=self.BUTTON_NEW_QUERY_ID).is_displayed()

    def previsit_questionnaire_button_visible(self):
        return self.driver.find_element(by=By.ID, value=self.BUTTON_PREVISIT_QUESTIONNAIRE_ID).is_displayed()

    def compliance_actions_button_visible(self):
        return self.driver.find_element(by=By.ID, value=self.BUTTON_COMPLIANCE_ACTIONS_ID).is_displayed()

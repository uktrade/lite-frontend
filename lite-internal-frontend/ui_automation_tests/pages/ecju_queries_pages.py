from shared.BasePage import BasePage
from shared.tools.helpers import select_visible_text_from_dropdown


class EcjuQueriesPages(BasePage):
    ADD_AN_ECJU_QUERY_BTN = '.govuk-button[href*="ecju-queries/add"]'
    QUERY_TYPE_DROP_DOWN = "picklist"
    QUESTION_TEXT_AREA = "question"
    CONFIRM_QUERY_CREATE_NO = '.govuk-radios__input[value="no"]'
    CONFIRM_QUERY_CREATE_YES = '.govuk-radios__input[value="yes"]'
    OPEN_QUESTIONS = "open-question"
    CLOSED_QUESTIONS = "closed-question"
    CLOSED_ANSWERS = "closed-answer"

    def click_add_an_ecju_query_btn(self):
        self.driver.find_element_by_css_selector(self.ADD_AN_ECJU_QUERY_BTN).click()

    def select_ecju_query_type(self, value):
        drop_down = self.driver.find_element_by_id(self.QUERY_TYPE_DROP_DOWN)
        select_visible_text_from_dropdown(drop_down, value)

    def get_question_text(self):
        return self.driver.find_element_by_id(self.QUESTION_TEXT_AREA).text

    def enter_question_text(self, text):
        self.driver.find_element_by_id(self.QUESTION_TEXT_AREA).send_keys(text)

    def click_confirm_query_create_no(self):
        self.driver.find_element_by_css_selector(self.CONFIRM_QUERY_CREATE_NO).click()

    def click_confirm_query_create_yes(self):
        self.driver.find_element_by_css_selector(self.CONFIRM_QUERY_CREATE_YES).click()

    def get_open_query_questions(self):
        return [i.text for i in self.driver.find_elements_by_id(self.OPEN_QUESTIONS)]

    def get_closed_query_questions(self):
        questions = ""
        for question in self.driver.find_elements_by_id(self.CLOSED_QUESTIONS):
            questions += question.text
        return questions

    def get_closed_query_answers(self):
        answers = ""
        for answer in self.driver.find_elements_by_id(self.CLOSED_ANSWERS):
            answers += answer.text
        return answers

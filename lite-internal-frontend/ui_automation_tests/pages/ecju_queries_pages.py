from helpers.BasePage import BasePage
from helpers.helpers import select_visible_text_from_dropdown


class EcjuQueriesPages(BasePage):
    add_an_ecju_query_btn = '.govuk-button[href*="ecju-queries/add"]'
    query_type_drop_down = 'picklist'
    question_text_area = 'question'
    confirm_query_create_no = '.govuk-radios__input[value="no"]'
    confirm_query_create_yes = '.govuk-radios__input[value="yes"]'
    open_questions = 'open-question'
    closed_questions = 'closed-question'
    closed_answers = 'closed-answer'

    def click_add_an_ecju_query_btn(self):
        self.driver.find_element_by_css_selector(self.add_an_ecju_query_btn).click()

    def select_ecju_query_type(self, value):
        drop_down = self.driver.find_element_by_id(self.query_type_drop_down)
        select_visible_text_from_dropdown(drop_down, value)

    def get_question_text(self):
        return self.driver.find_element_by_id(self.question_text_area).text

    def enter_question_text(self, text):
        self.driver.find_element_by_id(self.question_text_area).send_keys(text)

    def click_confirm_query_create_no(self):
        self.driver.find_element_by_css_selector(self.confirm_query_create_no).click()

    def click_confirm_query_create_yes(self):
        self.driver.find_element_by_css_selector(self.confirm_query_create_yes).click()

    def get_open_query_questions(self):
        return [i.text for i in self.driver.find_elements_by_id(self.open_questions)]

    def get_closed_query_questions(self):
        questions = ""
        for question in self.driver.find_elements_by_id(self.closed_questions):
            questions += question.text
        return questions

    def get_closed_query_answers(self):
        answers = ""
        for answer in self.driver.find_elements_by_id(self.closed_answers):
            answers += answer.text
        return answers

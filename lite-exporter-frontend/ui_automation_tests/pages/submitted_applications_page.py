import time

from shared.BasePage import BasePage


class SubmittedApplicationsPages(BasePage):
    INPUT_CASE_NOTE_ID = "input-case-note"
    BUTTON_POST_NOTE_ID = "button-case-note-post"
    LINK_CANCEL_NOTE_ID = "link-case-note-cancel"
    CASE_NOTES_TEXT = ".lite-application-note--exporter"  # CSS
    CASE_NOTE_DATE_TIME = ".lite-case-notes .govuk-hint"  # CSS
    CASE_NOTE_CHARACTER_WARNING = "case_note-warning"  # ID

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.INPUT_CASE_NOTE_ID}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).text

    def click_post_note_btn(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.BUTTON_POST_NOTE_ID).click()

    def click_cancel_btn(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.LINK_CANCEL_NOTE_ID).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTES_TEXT)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTE_DATE_TIME)[no].text

    def find_case_note_text_area(self):
        return self.driver.find_elements_by_id(self.INPUT_CASE_NOTE_ID)

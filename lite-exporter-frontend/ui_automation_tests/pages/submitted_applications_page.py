from typing import List

from shared.BasePage import BasePage


class SubmittedApplicationsPages(BasePage):
    INPUT_CASE_NOTE_ID = "input-case-note"
    BUTTON_POST_NOTE_ID = "button-case-note-post"
    LINK_CANCEL_NOTE_ID = "link-case-note-cancel"
    CASE_NOTE_CLASS = "lite-application-note"
    CASE_NOTE_EXPORTER_CLASS = "lite-application-note--exporter"
    CASE_NOTE_DATE_TIME_SELECTOR = ".lite-case-notes .govuk-hint"

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.INPUT_CASE_NOTE_ID}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).text

    def click_post_note_button(self):
        self.driver.find_element_by_id(self.BUTTON_POST_NOTE_ID).click()

    def click_cancel_button(self):
        self.driver.find_element_by_id(self.LINK_CANCEL_NOTE_ID).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_class_name(self.CASE_NOTE_EXPORTER_CLASS)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTE_DATE_TIME_SELECTOR)[no].text

    def find_case_note_text_area(self):
        return self.driver.find_elements_by_id(self.INPUT_CASE_NOTE_ID)

    def assert_case_notes_exists(self, notes: List[str]):
        """
        Takes a list of strings (each representing case note text)
        First asserts that the list of notes on the page is correct
        Then asserts that each case note exists
        """
        case_notes = self.driver.find_elements_by_class_name(self.CASE_NOTE_CLASS)
        assert len(case_notes) == len(notes)

        for case_note in case_notes:
            assert case_note.text in notes

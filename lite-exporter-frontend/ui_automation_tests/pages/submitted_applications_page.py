import time

from shared.BasePage import BasePage


class SubmittedApplicationsPages(BasePage):
    CASE_NOTE_FIELD = "case_note"  # id
    POST_NOTE_BTN = "button-post-note"  # id
    CANCEL_NOTE_BTN = "case-note-cancel-button"  # id
    CASE_NOTES_TEXT = ".lite-application-note--exporter"  # css
    CASE_NOTE_DATE_TIME = ".lite-case-notes .govuk-hint"  # css
    CASE_NOTE_CHARACTER_WARNING = "case_note-warning"  # id

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.CASE_NOTE_FIELD}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.CASE_NOTE_FIELD).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.CASE_NOTE_FIELD).text

    def click_post_note_btn(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.POST_NOTE_BTN).click()

    def click_cancel_btn(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.CANCEL_NOTE_BTN).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTES_TEXT)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTE_DATE_TIME)[no].text

    def get_text_of_case_note_warning(self):
        time.sleep(1)
        return self.driver.find_element_by_id(self.CASE_NOTE_CHARACTER_WARNING).text

    def get_disabled_attribute_of_post_note(self):
        return self.driver.find_element_by_id(self.POST_NOTE_BTN).get_attribute("disabled")

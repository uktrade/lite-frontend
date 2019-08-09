from selenium.webdriver.support.ui import Select
import time

from helpers.BasePage import BasePage


class ApplicationPage(BasePage):

    case_note_field = "case_note"  # id
    post_note_btn = "button-post-note"  # id
    cancel_note_btn = "case-note-cancel-button"  # id
    case_notes_text = ".lite-case-note"  # css
    case_note_date_time = ".lite-activity-item .govuk-hint"  # css
    case_note_character_warning = "case_note-warning"  # id
    documents_btn = '.govuk-button[href*="documents"]'  # css
    progress_app_btn = '.govuk-button[href*="manage"]'
    record_decision_btn = '.govuk-button[href*="decide"]'  # css
    headers = ".lite-heading-s"  # css
    activity_case_note_subject = ".lite-activity-item .govuk-body"
    activity_dates = ".lite-activity-item .govuk-hint"
    activity_user = ".user"
    is_visible_to_exporter_checkbox_id = 'is_visible_to_exporter'
    EDIT_CASE_FLAGS = 'application-edit-case-flags'  # ID
    view_advice = "a[href*='/advice-view/']"
    case_flags = 'application-case-flags'
    move_case_button = '.govuk-button[href*="move"]' # CSS
    status = 'status'  # ID
    audit_trail_item = '.lite-case-notes .lite-activity-item'  # CSS
    application_summary_board = '.lite-information-board'  # CSS
    destinations_table = 'destinations'  # ID

    def click_visible_to_exporter_checkbox(self):
        time.sleep(.5)
        self.driver.find_element_by_id(self.is_visible_to_exporter_checkbox_id).click()

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.case_note_field}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.case_note_field).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.case_note_field).text

    def click_post_note_btn(self):
        self.driver.find_element_by_id(self.post_note_btn).click()

    def click_cancel_btn(self):
        time.sleep(.5)
        self.driver.find_element_by_id(self.cancel_note_btn).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.case_notes_text)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.case_note_date_time)[no].text

    def get_text_of_case_note_warning(self):
        time.sleep(1)
        return self.driver.find_element_by_id(self.case_note_character_warning).text

    def get_disabled_attribute_of_post_note(self):
        return self.driver.find_element_by_id(self.post_note_btn).get_attribute("disabled")

    def get_class_name_of_post_note(self):
        return self.driver.find_element_by_id(self.post_note_btn).get_attribute("class")

    def click_progress_application(self):
        self.driver.find_element_by_css_selector(self.progress_app_btn).click()

    def click_record_decision(self):
        self.driver.find_element_by_css_selector(self.record_decision_btn).click()

    def click_documents_button(self):
        self.driver.find_element_by_css_selector(self.documents_btn).click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id(self.status))
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_case_note_subject(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_case_note_subject)[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_dates)[no].text

    def get_text_of_activity_users(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_user)[no].text

    def click_edit_case_flags(self):
        edit_cases_btn = self.driver.find_element_by_id(self.EDIT_CASE_FLAGS)
        edit_cases_btn.click()

    def click_view_advice(self):
        self.driver.find_element_by_css_selector(self.view_advice).click()

    def is_flag_applied(self, flag_id):
        case_flags = self.driver.find_element_by_id(self.case_flags)
        count = len(case_flags.find_elements_by_id(flag_id))
        return count == 1

    def click_move_case_button(self):
        self.driver.find_element_by_css_selector(self.move_case_button).click()

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.audit_trail_item)[no].text

    def get_text_of_application_summary_board(self):
        return self.driver.find_element_by_css_selector(self.application_summary_board).text

    def get_text_of_destinations_table(self):
        return self.driver.find_element_by_id(self.destinations_table).text

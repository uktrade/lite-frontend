from selenium.webdriver.support.ui import Select
import time

from helpers.BasePage import BasePage


class ApplicationPage(BasePage):

    actions_dropdown = ".app-more-actions__button"  # CSS
    case_note_field = "case_note"  # id
    post_note_btn = "button-post-note"  # id
    cancel_note_btn = "case-note-cancel-button"  # id
    case_notes_text = ".app-activity__additional-text"  # css
    case_note_date_time = ".app-activity__item .govuk-hint"  # css
    case_note_character_warning = "case_note-warning"  # id
    documents_btn = '[href*="documents"]'  # css
    ecju_queries_btn = '[href*="ecju-queries"]'  # css
    progress_app_btn = '[href*="manage"]'
    record_decision_btn = '[href*="decide"]'  # css
    headers = ".lite-heading-s"  # css
    activity_case_note_subject = ".lite-activity-item .govuk-body"
    activity_dates = ".app-activity__item .govuk-hint"
    activity_user = ".user"
    is_visible_to_exporter_checkbox_id = 'is_visible_to_exporter'
    edit_case_flags = 'application-edit-case-flags'  # ID
    edit_goods_flags = 'button-edit-goods-flags'  # ID
    checkbox_input = ".govuk-checkboxes__input"
    view_advice = 'a[href*="/user-advice-view/"]'
    case_flags = 'application-case-flags'
    move_case_button = '[href*="move"]' # CSS
    status = 'status'  # ID
    audit_trail_item = '.app-activity__item'  # CSS
    application_summary_board = '.lite-information-board'  # CSS
    eu_table = 'end-user'  # ID
    ueu_table = 'ultimate-end-users'  # ID
    consignee_table = 'consignee'  # ID
    third_parties_table = 'third-parties'  # ID
    give_advice_button = 'button-give-advice'  # ID
    checkbox = '[type="checkbox"]'  # CSS
    download_good_document = 'good_document'  # ID
    download_end_user_document = 'end_user_document'  # ID
    download_additional_document = 'additional_document'  # ID

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
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.progress_app_btn).click()

    def click_record_decision(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.record_decision_btn).click()

    def click_documents_button(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.documents_btn).click()

    def click_ecju_queries_button(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.ecju_queries_btn).click()

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
        edit_cases_btn = self.driver.find_element_by_id(self.edit_case_flags)
        edit_cases_btn.click()

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.edit_goods_flags)
        edit_goods_btn.click()

    def select_a_good(self):
        element = self.driver.find_element_by_css_selector(self.checkbox_input)
        self.driver.execute_script("arguments[0].click();", element)

    def click_view_advice(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.view_advice).click()

    def is_flag_applied(self, flag_id):
        count = len(self.driver.find_elements_by_id(flag_id))
        return count == 1

    def is_good_flag_applied(self, flag_name):
        return flag_name in self.driver.find_element_by_id("goods").text

    def click_move_case_button(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.move_case_button).click()

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.audit_trail_item)[no].text

    def get_text_of_application_summary_board(self):
        return self.driver.find_element_by_css_selector(self.application_summary_board).text

    def get_text_of_eu_table(self):
        return self.driver.find_element_by_id(self.eu_table).text

    def get_text_of_ueu_table(self):
        return self.driver.find_element_by_id(self.ueu_table).text

    def get_text_of_consignee_table(self):
        return self.driver.find_element_by_id(self.consignee_table).text

    def get_text_of_third_parties_table(self):
        return self.driver.find_element_by_id(self.third_parties_table).text

    def click_on_all_checkboxes(self):
        elements = self.driver.find_elements_by_css_selector(self.checkbox)
        num = 0
        for element in elements:
            element.click()
            num += 1
        self.driver.find_element_by_id(self.give_advice_button).click()
        return num

    def good_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.download_good_document).is_enabled()

    def end_user_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.download_end_user_document).is_enabled()

    def additional_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.download_additional_document).is_enabled()
from selenium.webdriver.support.ui import Select
import time

from helpers.BasePage import BasePage
from selenium.common.exceptions import NoSuchElementException


class ApplicationPage(BasePage):

    actions_dropdown = ".app-more-actions__button"  # CSS
    case_notification_anchor = "case-notification"  # ID
    audit_id = "[id^=case-activity-]"  # CSS
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
    activity_case_note_subject = ".govuk-body"
    activity_dates = ".app-activity__item .govuk-hint"
    activity_user = ".user"
    is_visible_to_exporter_checkbox_id = "is_visible_to_exporter"
    review_goods = "button-review-goods"
    edit_case_flags = "application-edit-case-flags"  # ID
    checkbox_input = ".govuk-checkboxes__input"
    view_advice = 'a[href*="/user-advice-view/"]'
    case_flags = "application-case-flags"
    move_case_button = '[href*="move"]'  # CSS
    status = "status"  # ID
    audit_trail_item = ".app-activity__item"  # CSS
    application_summary_board = ".govuk-summary-list"  # CSS
    eu_table = "end-user"  # ID
    ueu_table = "ultimate-end-users"  # ID
    consignee_table = "consignee"  # ID
    third_parties_table = "third-parties"  # ID
    give_advice_button = "button-give-advice"  # ID
    checkbox = '[type="checkbox"]'  # CSS
    download_good_document = "good_document"  # ID
    download_end_user_document = "end_user_document"  # ID
    download_additional_document = "additional_document"  # ID
    organisation = "applicant_organisation"  # CSS
    edit_goods_flags = "button-edit-goods-flags"  # ID

    goods_description_link = "#goods a"  # CSS

    def click_visible_to_exporter_checkbox(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.is_visible_to_exporter_checkbox_id).click()

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.case_note_field}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.case_note_field).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.case_note_field).text

    def click_post_note_btn(self):
        self.driver.find_element_by_id(self.post_note_btn).click()

    def click_cancel_btn(self):
        time.sleep(0.5)
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
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.progress_app_btn).click()

    def click_record_decision(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.record_decision_btn).click()

    def click_documents_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.documents_btn).click()

    def click_ecju_queries_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.ecju_queries_btn).click()

    def click_drop_down(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id(self.status))
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_case_note_subject(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_case_note_subject)[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_dates)[no].text

    def get_text_of_activity_users(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_user)[no].text

    def click_review_goods(self):
        self.driver.find_element_by_id(self.review_goods).click()

    def is_review_goods_button_present(self):
        try:
            self.driver.find_element_by_id(self.review_goods)
            return True
        except NoSuchElementException:
            return False

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.edit_goods_flags)
        edit_goods_btn.click()

    def click_edit_case_flags(self):
        edit_cases_btn = self.driver.find_element_by_id(self.edit_case_flags)
        edit_cases_btn.click()

    def select_a_good(self):
        element = self.driver.find_element_by_css_selector(self.checkbox_input)
        self.driver.execute_script("arguments[0].click();", element)

    def click_view_advice(self):
        self.driver.find_element_by_css_selector(self.actions_dropdown).click()
        self.driver.find_element_by_css_selector(self.view_advice).click()

    def is_flag_applied(self, flag_id):
        count = len(self.driver.find_elements_by_id(flag_id))
        return count > 0

    def is_good_flag_applied(self, flag_name):
        return flag_name in self.driver.find_element_by_id("goods").text

    def click_move_case_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.move_case_button).click()

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.audit_trail_item)[no].text

    def get_text_of_application_summary_board(self):
        return self.driver.find_element_by_css_selector(self.application_summary_board).text

    def get_text_of_eu_table(self):
        return self.driver.find_element_by_id(self.eu_table).text

    def get_case_notification_anchor(self):
        return self.driver.find_element_by_id(self.case_notification_anchor)

    def get_case_activity_id_by_audit_text(self, audit_text):
        audits = self.driver.find_elements_by_css_selector(self.audit_id)
        for audit in audits:
            if audit_text in audit.text:
                return audit.get_attribute("id")

        return None

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
            self.driver.execute_script("arguments[0].click();", element)
            num += 1
        self.driver.find_element_by_id(self.give_advice_button).click()
        return num

    def good_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.download_good_document).is_enabled()

    def end_user_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.download_end_user_document).is_enabled()

    def get_case_flag_element(self):
        return self.driver.find_element_by_id(self.case_flags)

    def get_document_element(self):
        return self.driver.find_element_by_css_selector(self.documents_btn)

    def get_move_case_element(self):
        return self.driver.find_element_by_css_selector(self.move_case_button)

    def get_ecju_queries_element(self):
        return self.driver.find_element_by_css_selector(self.ecju_queries_btn)

    def is_change_status_available(self):
        # this should equal 2 as there is a 'manage' in the link of the footer image
        return len(self.driver.find_elements_by_css_selector(self.progress_app_btn)) == 2

    def additional_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.download_additional_document).is_enabled()

    def go_to_organisation(self):
        element = self.driver.find_element_by_id(self.organisation)
        self.driver.execute_script("arguments[0].click();", element)

    def click_good_description_link(self):
        element = self.driver.find_element_by_css_selector(self.goods_description_link)
        self.driver.execute_script("arguments[0].click();", element)

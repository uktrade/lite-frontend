from selenium.webdriver.support.ui import Select
import time

from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id


class ApplicationPage(BasePage):
    ACTIONS_LIST_CONTAINER_ID = "actions-list"  # ID
    HEADING_ID = "heading-reference-code"
    ACTION_BUTTON_SELECTOR = "a"
    ACTIONS_DROPDOWN = ".lite-more-actions__button"  # CSS
    AUDIT_NOTIFICATION_ANCHOR = "audit-notification"  # ID
    AUDIT_CASE_ACTIVITY_ID = "[id^=case-activity-]"  # CSS
    INPUT_CASE_NOTE_ID = "input-case-note"
    BUTTON_POST_NOTE_ID = "button-case-note-post"
    LINK_CANCEL_NOTE_ID = "link-case-note-cancel"
    CASE_NOTES_TEXT = ".app-activity__item"  # css
    CASE_NOTE_DATE_TIME = ".app-activity__item .govuk-hint"  # css
    DOCUMENTS_BTN = '[href*="documents"]'  # css
    GENERATE_DOCUMENTS_BTN = "generate-document"  # id
    ECJU_QUERIES_BTN = '[href*="ecju-queries"]'  # css
    PROGRESS_APP_BTN = "change-status"  # ID
    ACTIVITY_CASE_NOTE_SUBJECT = ".app-activity__list .govuk-body"
    ACTIVITY_DATES = ".app-activity__item .govuk-hint"
    IS_VISIBLE_TO_EXPORTER_CHECKBOX_ID = "is_visible_to_exporter"
    REVIEW_GOODS = "button-review-goods"
    EDIT_CASE_FLAGS = "application-edit-case-flags"  # ID
    EDIT_DESTINATION_FLAGS_BUTTON = "button-edit-destinations-flags"  # ID
    CHECKBOX_INPUT = ".govuk-checkboxes__input"
    VIEW_ADVICE = 'a[href*="/user-advice-view/"]'
    CASE_FLAGS = "application-case-flags"
    MOVE_CASE_BUTTON = '[href*="move"]'  # CSS
    STATUS = "status"  # ID
    AUDIT_TRAIL_ITEM = ".app-activity__item"  # CSS
    APPLICATION_SUMMARY_BOARD = ".app-case-board"  # CSS
    TABLE_ENTITIES = "table-entities"  # ID
    TABLE_INACTIVE_ENTITIES_ID = "table-inactive-entities"  # ID
    GIVE_ADVICE_BUTTON = "button-give-advice"  # ID
    CHECKBOX = '[type="checkbox"]'  # CSS
    DOWNLOAD_GOOD_DOCUMENT = "good_document"  # ID
    DOWNLOAD_END_USER_DOCUMENT = "end_user_document"  # ID
    DOWNLOAD_ADDITIONAL_DOCUMENT = "supporting-documentation"  # ID
    LINK_ORGANISATION_ID = "link-organisation"
    EDIT_GOODS_FLAGS = "button-edit-goods-flags"  # ID
    CASE_OFFICER_ID = "case-officer"  # ID
    LINK_ADDITIONAL_CONTACTS_ID = "link-additional-contacts"
    ASSIGN_USER_ID = "assign-user"
    EXPAND_FLAGS_PARTIAL_ID = "expand-flags-"
    ASSIGNED_USERS_ID = "assigned_users"
    CASE_QUEUES_ID = "case_queues"
    HMRC_GOODS_LOCATION = "hmrc-goods-location"
    CASE_COPY_OF_ID = "case-copy-of"
    TYPE_OF_CASE = "case-type"  # ID
    DESTINATION_CHECKBOX = "destinations"  # NAME
    IM_DONE_BUTTON_ID = "done"
    CASE_LINK_PARTIAL_ID = "case-"

    def get_case_copy_of_field_href(self):
        return self.driver.find_element_by_id(self.CASE_COPY_OF_ID).get_attribute("href")

    def click_visible_to_exporter_checkbox(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.IS_VISIBLE_TO_EXPORTER_CHECKBOX_ID).click()

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.INPUT_CASE_NOTE_ID}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).text

    def click_post_note_btn(self):
        self.driver.find_element_by_id(self.BUTTON_POST_NOTE_ID).click()

    def click_cancel_btn(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.LINK_CANCEL_NOTE_ID).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTES_TEXT)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTE_DATE_TIME)[no].text

    def click_progress_application(self):
        self.click_drop_down()
        scroll_to_element_by_id(self.driver, self.PROGRESS_APP_BTN)
        self.driver.find_element_by_id(self.PROGRESS_APP_BTN).click()

    def click_documents_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.DOCUMENTS_BTN).click()

    def click_generate_document_button(self):
        self.click_drop_down()
        self.driver.find_element_by_id(self.GENERATE_DOCUMENTS_BTN).click()

    def click_ecju_queries_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.ECJU_QUERIES_BTN).click()

    def click_case_officer_button(self):
        self.click_drop_down()
        scroll_to_element_by_id(self.driver, self.CASE_OFFICER_ID)
        self.driver.find_element_by_id(self.CASE_OFFICER_ID).click()

    def click_additional_contacts_link(self):
        self.click_drop_down()
        scroll_to_element_by_id(self.driver, self.LINK_ADDITIONAL_CONTACTS_ID)
        self.driver.find_element_by_id(self.LINK_ADDITIONAL_CONTACTS_ID).click()

    def click_drop_down(self):
        # This is going to be removed as part of the case refactor
        self.driver.find_element_by_css_selector(self.ACTIONS_DROPDOWN).click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id(self.STATUS))
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_case_note_subject(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_CASE_NOTE_SUBJECT)[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_DATES)[no].text

    def click_review_goods(self):
        self.driver.find_element_by_id(self.REVIEW_GOODS).click()

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.EDIT_GOODS_FLAGS)
        edit_goods_btn.click()

    def click_edit_case_flags(self):
        edit_cases_btn = self.driver.find_element_by_id(self.EDIT_CASE_FLAGS)
        edit_cases_btn.click()

    def click_edit_destination_flags(self):
        self.driver.find_element_by_name(self.DESTINATION_CHECKBOX).click()
        edit_destination_flags_btn = self.driver.find_element_by_id(self.EDIT_DESTINATION_FLAGS_BUTTON)
        edit_destination_flags_btn.click()

    def select_a_good(self):
        element = self.driver.find_element_by_css_selector(self.CHECKBOX_INPUT)
        self.driver.execute_script("arguments[0].click();", element)

    def click_view_advice(self):
        self.driver.find_element_by_css_selector(self.ACTIONS_DROPDOWN).click()
        self.driver.find_element_by_css_selector(self.VIEW_ADVICE).click()

    def is_flag_applied(self, flag_id):
        count = len(self.driver.find_elements_by_id(flag_id))
        return count > 0

    def is_good_flag_applied(self, flag_name):
        return flag_name in self.driver.find_element_by_id("goods").text

    def click_move_case_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.MOVE_CASE_BUTTON).click()

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)[no].text

    def get_text_of_application_summary_board(self):
        return self.driver.find_element_by_css_selector(self.APPLICATION_SUMMARY_BOARD).text

    def get_text_of_eu_table(self):
        return self.driver.find_element_by_id(self.TABLE_ENTITIES).text

    def get_case_notification_anchor(self):
        return self.driver.find_element_by_id(self.AUDIT_NOTIFICATION_ANCHOR)

    def get_case_activity_id_by_audit_text(self, old_text, new_text):
        audits = self.driver.find_elements_by_css_selector(self.AUDIT_CASE_ACTIVITY_ID)
        for audit in audits:
            if old_text in audit.text and new_text in audit.text:
                return audit.get_attribute("id")

        return None

    def get_text_of_ueu_table(self):
        return self.driver.find_element_by_id(self.TABLE_ENTITIES).text

    def get_text_of_consignee_table(self):
        return self.driver.find_element_by_id(self.TABLE_ENTITIES).text

    def get_text_of_third_parties_table(self):
        return self.driver.find_element_by_id(self.TABLE_ENTITIES).text

    def get_text_of_inactive_entities_table(self):
        return self.driver.find_element_by_id(self.TABLE_INACTIVE_ENTITIES_ID).text

    def click_on_all_checkboxes(self):
        elements = self.driver.find_elements_by_css_selector(self.CHECKBOX)
        num = 0
        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)
            num += 1
        self.driver.find_element_by_id(self.GIVE_ADVICE_BUTTON).click()
        return num

    def good_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_GOOD_DOCUMENT).is_enabled()

    def end_user_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_END_USER_DOCUMENT).is_enabled()

    def get_case_flag_element(self):
        return self.driver.find_element_by_id(self.CASE_FLAGS)

    def get_document_element(self):
        return self.driver.find_element_by_css_selector(self.DOCUMENTS_BTN)

    def get_move_case_element(self):
        return self.driver.find_element_by_css_selector(self.MOVE_CASE_BUTTON)

    def get_ecju_queries_element(self):
        return self.driver.find_element_by_css_selector(self.ECJU_QUERIES_BTN)

    def get_case_officer_element(self):
        return self.driver.find_element_by_id(self.CASE_OFFICER_ID)

    def get_additional_contacts_element(self):
        return self.driver.find_element_by_id(self.LINK_ADDITIONAL_CONTACTS_ID)

    def get_assign_user_element(self):
        return self.driver.find_element_by_id(self.ASSIGN_USER_ID)

    def get_generate_document_element(self):
        return self.driver.find_element_by_id(self.GENERATE_DOCUMENTS_BTN)

    def is_change_status_available(self):
        return len(self.driver.find_elements_by_id(self.PROGRESS_APP_BTN)) == 1

    def additional_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_ADDITIONAL_DOCUMENT).is_enabled()

    def go_to_organisation(self):
        self.driver.find_element_by_id(self.LINK_ORGANISATION_ID).click()

    def get_action_dropdown_entries_count(self):
        return len(
            self.driver.find_element_by_id(self.ACTIONS_LIST_CONTAINER_ID).find_elements_by_css_selector(
                self.ACTION_BUTTON_SELECTOR
            )
        )

    def click_expand_flags(self, case_id):
        self.driver.find_element_by_id(self.EXPAND_FLAGS_PARTIAL_ID + case_id).click()

    def get_type_of_case_from_page(self):
        return self.driver.find_element_by_id(self.TYPE_OF_CASE).text

    def click_assign_user_button(self):
        self.click_drop_down()
        scroll_to_element_by_id(self.driver, self.ASSIGN_USER_ID)
        self.driver.find_element_by_id(self.ASSIGN_USER_ID).click()

    def click_im_done_button(self):
        self.driver.find_element_by_id(self.IM_DONE_BUTTON_ID).click()

    def click_on_case_link(self, case_id):
        self.driver.find_element_by_id(self.CASE_LINK_PARTIAL_ID + case_id).click()

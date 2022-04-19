from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_by_id
from tests_common.tools.helpers import scroll_to_element_below_header_by_id


class ApplicationPage(BasePage):
    ACTIONS_LIST_CONTAINER_ID = "actions-list"  # ID
    HEADING_ID = "heading-reference-code"
    ACTION_BUTTON_SELECTOR = "a"
    AUDIT_NOTIFICATION_ANCHOR = "audit-notification"  # ID
    AUDIT_CASE_ACTIVITY_ID = "[id^=case-activity-]"  # CSS
    INPUT_CASE_NOTE_ID = "input-case-note"
    BUTTON_POST_NOTE_ID = "button-case-note-post"
    LINK_CANCEL_NOTE_ID = "link-case-note-cancel"
    CASE_NOTES_TEXT = ".app-activity__item"  # css
    CASE_NOTE_DATE_TIME = ".app-activity__item .govuk-hint"  # css
    DOCUMENTS_BTN = "tab-documents"  # ID
    GENERATE_DOCUMENTS_BTN = "button-generate-document"  # id
    ECJU_QUERIES_BTN = '[href*="ecju-queries"]'  # css
    PROGRESS_APP_BTN = "change-status"  # ID
    CONFIRM_RERUN_ROUTING_RULES = "confirm-yes"
    ACTIVITY_CASE_NOTE_SUBJECT = ".app-activity__list .govuk-body"
    ACTIVITY_DATES = ".app-activity__item .govuk-hint"
    IS_VISIBLE_TO_EXPORTER_CHECKBOX_ID = "is_visible_to_exporter"
    BUTTON_REVIEW_GOODS_ID = "button-review-goods"
    EDIT_CASE_FLAGS = "link-change-flags"  # ID
    BUTTON_EDIT_DESTINATION_FLAGS_ID = "button-edit-destinations-flags"
    CHECKBOX_INPUT = ".govuk-checkboxes__input"
    MOVE_CASE_BUTTON = "link-change-queues"  # ID
    STATUS = "status"  # ID
    AUDIT_TRAIL_ITEM = ".app-activity__item"  # CSS
    APPLICATION_SUMMARY_BOARD = ".app-case-board"  # CSS
    TABLE_ENTITIES = "table-destinations"  # ID
    TABLE_INACTIVE_ENTITIES_ID = "table-inactive-entities"  # ID
    CHECKBOX = '[type="checkbox"]'  # CSS
    DOWNLOAD_GOOD_DOCUMENT = "good_document"  # ID
    DOWNLOAD_END_USER_DOCUMENT = "link-end_user-download"  # ID
    DOWNLOAD_ADDITIONAL_DOCUMENT = "supporting-documentation"  # ID
    LINK_ORGANISATION_ID = "link-organisation"
    EDIT_GOODS_FLAGS = "button-edit-goods-flags"  # ID
    CASE_OFFICER_CSS = ".govuk-link[href*='case-officer']"  # CSS
    ASSIGN_USER_ID = "assign-user"
    EXPAND_FLAGS_CSS = ".app-flags__expander"
    ASSIGNED_USERS_ID = "assigned-users"
    CASE_QUEUES_ID = "assigned-queues"
    HMRC_GOODS_LOCATION = "hmrc-goods-location"
    CASE_COPY_OF_ID = "link-case-copy-of"
    TYPE_OF_CASE = "case-type"  # ID
    BUTTON_IM_DONE_ID = "button-done"
    CASE_LINK_PARTIAL_ID = "case-"
    USER_TYPE_ID = "user_type"
    CASE_NOTES_AND_ACTIVITY_TAB = "tab-activity"  # ID
    TABLE_GOODS_ID = "table-goods"
    TABLE_DESTINATIONS_ID = "table-destinations"
    NEXT_REVIEW_DATE_DAY_ID = "next_review_dateday"
    NEXT_REVIEW_DATE_MONTH_ID = "next_review_datemonth"
    NEXT_REVIEW_DATE_YEAR_ID = "next_review_dateyear"
    COUNTERSIGN_NOTE_ID = "note"

    def get_case_copy_of_field_href(self):
        return self.driver.find_element_by_id(self.CASE_COPY_OF_ID).get_attribute("href")

    def click_visible_to_exporter_checkbox(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.IS_VISIBLE_TO_EXPORTER_CHECKBOX_ID))
        ).click()

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.INPUT_CASE_NOTE_ID}").value = "{text[:-1]}"')
        self.driver.find_element(by=By.ID, value=self.INPUT_CASE_NOTE_ID).send_keys(text[-1:])

    def enter_countersign_note(self, text):
        self.driver.find_element(by=By.ID, value=self.COUNTERSIGN_NOTE_ID).send_keys(text)

    def set_next_review_date(self, day, month, year, context):
        self.driver.find_element_by_id(self.NEXT_REVIEW_DATE_DAY_ID).clear()
        self.driver.find_element_by_id(self.NEXT_REVIEW_DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.NEXT_REVIEW_DATE_MONTH_ID).clear()
        self.driver.find_element_by_id(self.NEXT_REVIEW_DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.NEXT_REVIEW_DATE_YEAR_ID).clear()
        self.driver.find_element_by_id(self.NEXT_REVIEW_DATE_YEAR_ID).send_keys(year)

        context.next_review_date = f"{year}-{month}-{day}"

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.INPUT_CASE_NOTE_ID).text

    def click_post_note_btn(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.BUTTON_POST_NOTE_ID))
        )

        self.driver.find_element(by=By.ID, value=self.BUTTON_POST_NOTE_ID).click()

    def click_cancel_btn(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.LINK_CANCEL_NOTE_ID))
        ).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=self.CASE_NOTES_TEXT)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=self.CASE_NOTE_DATE_TIME)[no].text

    def click_progress_application(self):
        scroll_to_element_by_id(self.driver, self.PROGRESS_APP_BTN)
        self.driver.find_element_by_id(self.PROGRESS_APP_BTN).click()

    def click_confirm_rerun_routing_rules(self):
        self.driver.find_element_by_id(self.CONFIRM_RERUN_ROUTING_RULES).click()

    def click_documents_button(self):
        self.driver.find_element_by_id(self.DOCUMENTS_BTN).click()

    def click_generate_document_button(self):
        self.driver.find_element_by_id(self.GENERATE_DOCUMENTS_BTN).click()

    def select_status(self, status):
        scroll_to_element_below_header_by_id(self.driver, self.STATUS)
        case_status_dropdown = Select(self.driver.find_element_by_id(self.STATUS))
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_case_note_subject(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_CASE_NOTE_SUBJECT)[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_DATES)[no].text

    def click_review_goods(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_REVIEW_GOODS_ID).click()

    def click_on_notes_and_timeline(self):
        self.driver.find_element(by=By.ID, value=self.CASE_NOTES_AND_ACTIVITY_TAB).click()

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.EDIT_GOODS_FLAGS)
        edit_goods_btn.click()

    def click_edit_case_flags(self):
        edit_cases_btn = self.driver.find_element_by_id(self.EDIT_CASE_FLAGS)
        edit_cases_btn.click()

    def click_edit_destination_flags(self):
        edit_destination_flags_btn = self.driver.find_element_by_id(self.BUTTON_EDIT_DESTINATION_FLAGS_ID)
        edit_destination_flags_btn.click()

    def select_a_good(self):
        element = self.driver.find_element_by_css_selector(self.CHECKBOX_INPUT)
        self.driver.execute_script("arguments[0].click();", element)

    def click_move_case_button(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.MOVE_CASE_BUTTON))
        ).click()

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)[no].text

    def get_text_of_audit_trail(self):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM).text

    def get_text_of_application_summary_board(self):
        return self.driver.find_element_by_css_selector(self.APPLICATION_SUMMARY_BOARD).text

    def get_text_of_eu_table(self):
        return self.driver.find_element_by_id(self.TABLE_ENTITIES).text

    def get_case_notification_anchor(self):
        return self.driver.find_elements_by_css_selector(".lite-tabs__tab .lite-tabs__tab-notification")

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

    def good_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_GOOD_DOCUMENT).is_enabled()

    def end_user_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_END_USER_DOCUMENT).is_enabled()

    def get_document_element(self):
        return self.driver.find_element_by_css_selector(self.DOCUMENTS_BTN)

    def get_move_case_element(self):
        return self.driver.find_element_by_id(self.MOVE_CASE_BUTTON)

    def get_ecju_queries_element(self):
        return self.driver.find_element_by_css_selector(self.ECJU_QUERIES_BTN)

    def get_case_officer_element(self):
        return self.driver.find_element_by_css_selector(self.CASE_OFFICER_CSS)

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

    def click_expand_flags(self, element, num):
        element.self.driver.find_elements_by_css_selector(self.EXPAND_FLAGS_CSS)[num].click()

    def get_type_of_case_from_page(self):
        return self.driver.find_element_by_id(self.TYPE_OF_CASE).text

    def click_assign_user_button(self):
        scroll_to_element_by_id(self.driver, self.ASSIGN_USER_ID)
        self.driver.find_element_by_id(self.ASSIGN_USER_ID).click()

    def click_im_done_button(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.BUTTON_IM_DONE_ID))
        ).click()

    def click_on_case_link(self, case_id):
        self.driver.find_element_by_id(self.CASE_LINK_PARTIAL_ID + case_id).click()

    def get_case_queues(self):
        return self.driver.find_element_by_id(self.CASE_QUEUES_ID)

    def select_filter_user_type_from_dropdown(self, user_type):
        functions.try_open_filters(self.driver)
        select = Select(self.driver.find_element_by_id(self.USER_TYPE_ID))
        select.select_by_visible_text(user_type)
        functions.click_apply_filters(self.driver)

    def get_text_of_first_audit_trail_item(self):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)[-1].text

    def get_audit_elements(self):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)

    def go_to_cases_activity_tab(self, internal_url, context):
        self.driver.get(
            internal_url.rstrip("/")
            + "/queues/00000000-0000-0000-0000-000000000001/cases/"
            + context.case_id
            + "/activity/"
        )

    def go_to_cases_activity_tab_for_clc(self, internal_url, context):
        self.driver.get(
            internal_url.rstrip("/")
            + "/queues/00000000-0000-0000-0000-000000000001/cases/"
            + context.clc_case_id
            + "/activity/"
        )

    def go_to_cases_activity_tab_for_pv(self, internal_url, context):
        self.driver.get(
            internal_url.rstrip("/")
            + "/queues/00000000-0000-0000-0000-000000000001/cases/"
            + context.pv_case_id
            + "/activity/"
        )

    def go_to_cases_activity_tab_for_eua(self, internal_url, context):
        self.driver.get(
            internal_url.rstrip("/")
            + "/queues/00000000-0000-0000-0000-000000000001/cases/"
            + context.eua_id
            + "/activity/"
        )

    def select_end_user(self, end_user_name):
        self.driver.find_element(
            by=By.XPATH,
            value=f"//input[@type='checkbox' and @name='end_user' and ancestor::tr/td/text()[contains(., '{end_user_name}')]]",
        ).click()

    def get_matches(self, match_type):
        """Return a list of names that have denial matches based on
        the supplied match_type - one of "PARTIAL MATCH" or "EXACT MATCH".
        """
        table = WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='table-denial-matches']"))
        )

        return [
            td.text
            for td in table.find_elements(
                by=By.XPATH, value=f"tbody/tr/td[3][contains(preceding-sibling::td/strong/text(), '{match_type}')]"
            )
        ]

    def select_denial_match(self, name):
        return self.driver.find_element(
            by=By.XPATH,
            value=f"//input[@type='checkbox' and ancestor::table[@id='table-denial-matches']/tbody/tr/td[3][contains(text(), '{name}')]]",
        ).click()

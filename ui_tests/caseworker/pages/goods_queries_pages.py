from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_below_header_by_id
from tests_common.tools.helpers import scroll_to_element_by_id


class GoodsQueriesPages(BasePage):
    CONTROL_RESPONSE = "-is_good_controlled"  # Name suffix
    TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR = "div#control_list_entries input.tokenfield-input"
    REPORT_SUMMARY = "-report_summary"  # Name suffix
    COMMENT = "-comment"  # ID
    SUBMIT_BUTTON = '.govuk-button[type*="great-mvp-wizard-step-button"]'  # CSS
    CASE_CLOSE_INFO_BAR_ID = "banner-case-closed"
    BUTTON_CLC_RESPOND_ID = "clc-button-respond"
    BUTTON_GRADING_RESPOND_ID = "grading-button-respond"
    PREFIX_ID = "prefix"
    SUFFIX_ID = "suffix"
    GRADING_ID = "grading"
    LINK_REPORT_SUMMARY_PICKLIST_PICKER_ID = "link-report_summary-picklist-picker"
    LINK_PICKLIST_PICKER_ITEM_CLASS = "app-picklist-picker__item"
    BUTTON_SUBMIT_REPORT_SUMMARY_ID = "button-submit-report_summary"
    STEP_NAME = None

    def click_respond_to_clc_query(self):
        scroll_to_element_below_header_by_id(self.driver, self.BUTTON_CLC_RESPOND_ID)
        self.driver.find_element_by_id(self.BUTTON_CLC_RESPOND_ID).click()

    def click_respond_to_grading_query(self):
        scroll_to_element_below_header_by_id(self.driver, self.BUTTON_GRADING_RESPOND_ID)
        self.driver.find_element_by_id(self.BUTTON_GRADING_RESPOND_ID).click()

    def type_in_to_control_list_entry(self, code):
        functions.send_tokens_to_token_bar(self.driver, self.TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR, [code])

    def choose_report_summary(self):
        scroll_to_element_by_id(self.driver, self.LINK_REPORT_SUMMARY_PICKLIST_PICKER_ID)
        self.driver.find_element_by_id(self.LINK_REPORT_SUMMARY_PICKLIST_PICKER_ID).click()
        self.driver.find_elements_by_class_name(self.LINK_PICKLIST_PICKER_ITEM_CLASS)[0].click()
        self.driver.find_element_by_id(self.BUTTON_SUBMIT_REPORT_SUMMARY_ID).click()

    def enter_a_prefix(self, prefix):
        self.driver.find_element_by_id(self.PREFIX_ID).send_keys(prefix)

    def select_a_grading(self, grading):
        Select(self.driver.find_element_by_id(self.GRADING_ID)).select_by_visible_text(grading)

    def enter_a_suffix(self, suffix):
        self.driver.find_element_by_id(self.SUFFIX_ID).send_keys(suffix)

    def is_clc_query_case_closed(self):
        return len(self.driver.find_elements_by_id(self.CASE_CLOSE_INFO_BAR_ID)) == 1

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BUTTON).click()

    def enter_a_comment(self, comment):
        comment_el = self.driver.find_element_by_name(f"{self.good_pk}{self.COMMENT}")
        comment_el.send_keys(comment)

    def enter_ars(self, ars_text):
        ars_el = self.driver.find_element_by_name(f"{self.good_pk}{self.REPORT_SUMMARY}")
        ars_el.send_keys(ars_text)

    def click_is_good_controlled(self, answer):
        good_selector = f"input[name='{self.good_pk}{self.CONTROL_RESPONSE}'][value={answer}]"
        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, good_selector))
        ).click()

    @property
    def good_pk(self):
        if not hasattr(self, "_good_pk"):
            step_input = self.driver.find_element_by_name(self.STEP_NAME)
            self._good_pk = step_input.get_attribute("value")
        return self._good_pk


class OpenGoodsReviewPages(GoodsQueriesPages):
    STEP_NAME = "review_open_application_good_wizard_view-current_step"


class StandardGoodsReviewPages(GoodsQueriesPages):
    STEP_NAME = "review_standard_application_good_wizard_view-current_step"

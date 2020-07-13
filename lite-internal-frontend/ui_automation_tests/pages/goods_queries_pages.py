from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from shared import functions
from pages.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_below_header_by_id
from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id


class GoodsQueriesPages(BasePage):
    CONTROL_RESPONSE = "is_good_controlled-"  # ID
    TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR = "#pane_control_list_entries .tokenfield-input"
    REPORT_SUMMARY = "report_summary"  # Name
    COMMENT = "comment"  # ID
    CASE_CLOSE_INFO_BAR_ID = "banner-case-closed"
    BUTTON_CLC_RESPOND_ID = "clc-button-respond"
    BUTTON_GRADING_RESPOND_ID = "grading-button-respond"
    SUBMIT_BUTTON = '.govuk-button[type*="submit"]'  # CSS
    PREFIX_ID = "prefix"
    SUFFIX_ID = "suffix"
    GRADING_ID = "grading"
    LINK_REPORT_SUMMARY_PICKLIST_PICKER_ID = "link-report_summary-picklist-picker"
    LINK_PICKLIST_PICKER_ITEM_CLASS = "app-picklist-picker__item"
    BUTTON_SUBMIT_REPORT_SUMMARY_ID = "button-submit-report_summary"

    def click_respond_to_clc_query(self):
        scroll_to_element_below_header_by_id(self.driver, self.BUTTON_CLC_RESPOND_ID)
        self.driver.find_element_by_id(self.BUTTON_CLC_RESPOND_ID).click()

    def click_respond_to_grading_query(self):
        scroll_to_element_below_header_by_id(self.driver, self.BUTTON_GRADING_RESPOND_ID)
        self.driver.find_element_by_id(self.BUTTON_GRADING_RESPOND_ID).click()

    def click_is_good_controlled(self, answer):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, self.CONTROL_RESPONSE + answer))
        ).click()

    def type_in_to_control_list_entry(self, code):
        functions.send_tokens_to_token_bar(self.driver, self.TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR, [code])

    def choose_report_summary(self):
        self.driver.find_element_by_id(self.LINK_REPORT_SUMMARY_PICKLIST_PICKER_ID).click()
        self.driver.find_elements_by_class_name(self.LINK_PICKLIST_PICKER_ITEM_CLASS)[0].click()
        self.driver.find_element_by_id(self.BUTTON_SUBMIT_REPORT_SUMMARY_ID).click()

    def enter_a_comment(self, comment):
        self.driver.implicitly_wait(0)
        if self.driver.find_element_by_class_name("govuk-details").get_attribute("open") is None:
            self.driver.find_element_by_class_name("govuk-details__summary-text").click()
        self.driver.implicitly_wait(10)
        scroll_to_element_by_id(self.driver, self.COMMENT)
        self.driver.find_element_by_id(self.COMMENT).send_keys(comment)

    def enter_a_prefix(self, prefix):
        self.driver.find_element_by_id(self.PREFIX_ID).send_keys(prefix)

    def select_a_grading(self, grading):
        Select(self.driver.find_element_by_id(self.GRADING_ID)).select_by_visible_text(grading)

    def enter_a_suffix(self, suffix):
        self.driver.find_element_by_id(self.SUFFIX_ID).send_keys(suffix)

    def is_clc_query_case_closed(self):
        return len(self.driver.find_elements_by_id(self.CASE_CLOSE_INFO_BAR_ID)) == 1

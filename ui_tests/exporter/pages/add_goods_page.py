from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from tests_common import functions
from ui_tests.exporter.pages.BasePage import BasePage


class AddGoodPage(BasePage):
    # Confirm has document
    DOCUMENT_VALID_YES = "has_document_to_upload-yes"  # ID
    DOCUMENT_VALID_NO = "has_document_to_upload-no"  # ID
    ECJU_HELPLINE_ID = "conditional-has_document_to_upload-no-conditional"
    MISSING_DOCUMENT_REASON = "missing_document_reason"  # ID

    # Good summary page
    GOOD_SUMMARY = ".govuk-summary-list"  # CSS

    # Add a good
    PART_NUMBER = "part_number"  # ID
    IS_CONTROLLED = "is_good_controlled"
    IS_PV_GRADED = "is_pv_graded"
    TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR = "#control_list_entries .tokenfield-input"
    DESCRIPTION = "description"  # ID

    # Not sure form
    UNSURE_CLC_CODE = "clc_control_code"  # ID
    UNSURE_CLC_DETAILS = "clc_raised_reasons"  # ID
    UNSURE_PV_GRADING_DETAILS = "pv_grading_raised_reasons"  # ID

    def input_element_by_id(self, id, text):
        element = self.driver.find_element_by_id(id)
        element.clear()
        element.send_keys(text)

    def enter_good_name(self, name):
        self.driver.find_element(by=By.XPATH, value="//input[@type='text' and contains(@id, 'name')]").send_keys(name)

    def enter_description_of_goods(self, description):
        self.input_element_by_id(self.DESCRIPTION, description)

    def select_is_your_good_controlled(self, option):
        # The only options accepted here are True and False
        self._select_radio(self.IS_CONTROLLED, option)

    def select_is_your_good_graded(self, option):
        # The only options accepted here are 'yes' and 'no'
        self._select_radio(self.IS_PV_GRADED, option)

    def _select_radio(self, identifier, option):
        self.driver.find_element(
            by=By.XPATH, value=f"//input[@type='radio' and contains(@id, '{identifier}') and @value='{option}']"
        ).click()

    def enter_control_list_entries(self, control_list_entry: str):
        functions.send_tokens_to_token_bar(
            self.driver, self.TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR, [control_list_entry]
        )

    def enter_control_code_unsure(self, code):
        control_code_tb = self.driver.find_element_by_id(self.UNSURE_CLC_CODE)
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def enter_control_unsure_details(self, details):
        unsure_details = self.driver.find_element_by_id(self.UNSURE_CLC_DETAILS)
        unsure_details.clear()
        unsure_details.send_keys(details)

    def enter_grading_unsure_details(self, details):
        unsure_pv_details = self.driver.find_element_by_id(self.UNSURE_PV_GRADING_DETAILS)
        unsure_pv_details.clear()
        unsure_pv_details.send_keys(details)

    def enter_part_number(self, part_number):
        part_number_tb = self.driver.find_element_by_id(self.PART_NUMBER)
        part_number_tb.clear()
        part_number_tb.send_keys(part_number)

    def confirm_can_upload_good_document(self):
        self.driver.find_element_by_id(self.DOCUMENT_VALID_YES).click()

    def confirm_cannot_upload_good_document(self):
        self.driver.find_element_by_id(self.DOCUMENT_VALID_NO).click()

    def get_ecju_help(self):
        return self.driver.find_element_by_id(self.ECJU_HELPLINE_ID).is_displayed()

    def select_valid_missing_document_reason(self):
        Select(self.driver.find_element_by_id(self.MISSING_DOCUMENT_REASON)).select_by_index(1)

    def get_good_summary_text(self):
        return self.driver.find_element_by_css_selector(self.GOOD_SUMMARY).text

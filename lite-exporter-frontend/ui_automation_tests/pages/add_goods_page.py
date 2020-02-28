from selenium.webdriver.support.select import Select

from ui_automation_tests.shared.BasePage import BasePage


class AddGoodPage(BasePage):
    # Confirm has document
    DOCUMENT_VALID_YES = "has_document_to_upload-yes"  # ID
    DOCUMENT_VALID_NO = "has_document_to_upload-no"  # ID
    ECJU_HELPLINE = "pane_ecju_contact"  # ID
    MISSING_DOCUMENT_REASON = "missing_document_reason"  # ID

    # Good summary page
    GOOD_SUMMARY = ".govuk-summary-list"  # CSS

    # Add a good
    PART_NUMBER = "part_number"  # ID
    IS_CONTROLLED = "is_good_controlled-"  # Partial ID
    IS_PV_GRADED = "is_pv_graded-"
    CONTROL_CODE = "control_code"  # ID
    DESCRIPTION = "description"  # ID

    # Not sure form
    UNSURE_CLC_CODE = "clc_control_code"  # ID
    UNSURE_CLC_DETAILS = "clc_raised_reasons"  # ID
    UNSURE_PV_GRADING_DETAILS = "pv_grading_raised_reasons"  # ID

    def enter_description_of_goods(self, description):
        self.driver.find_element_by_id(self.DESCRIPTION).send_keys(description)

    def select_is_your_good_controlled(self, option):
        # The only options accepted here are 'yes', 'no' and 'unsure'
        self.driver.find_element_by_id(self.IS_CONTROLLED + option.lower()).click()

    def select_is_your_good_graded(self, option):
        # The only options accepted here are 'yes', 'no' and 'grading_required'
        self.driver.find_element_by_id(self.IS_PV_GRADED + option.lower()).click()

    def enter_control_code(self, code):
        control_code_tb = self.driver.find_element_by_id(self.CONTROL_CODE)
        control_code_tb.clear()
        control_code_tb.send_keys(code)

        # This is done as control code textbox needs to lose focus
        self.driver.find_element_by_id(self.DESCRIPTION).click()

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
        return self.driver.find_element_by_id(self.ECJU_HELPLINE).is_displayed()

    def select_valid_missing_document_reason(self):
        Select(self.driver.find_element_by_id(self.MISSING_DOCUMENT_REASON)).select_by_index(1)

    def get_good_summary_text(self):
        return self.driver.find_element_by_css_selector(self.GOOD_SUMMARY).text

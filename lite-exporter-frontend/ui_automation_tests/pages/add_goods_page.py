from selenium.webdriver.support.select import Select

from shared.BasePage import BasePage


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
    CONTROL_CODE = "control_code"  # ID
    DESCRIPTION = "description"  # ID

    # Not sure form
    UNSURE_CODE = "not_sure_details_control_code"  # ID
    UNSURE_DETAILS = "not_sure_details_details"  # ID

    def enter_description_of_goods(self, description):
        self.driver.find_element_by_id(self.DESCRIPTION).send_keys(description)

    def select_is_your_good_controlled(self, option):
        # The only options accepted here are 'yes', 'no' and 'unsure'
        self.driver.find_element_by_id(self.IS_CONTROLLED + option.lower()).click()

    def enter_control_code(self, code):
        control_code_tb = self.driver.find_element_by_id(self.CONTROL_CODE)
        control_code_tb.clear()
        control_code_tb.send_keys(code)

        # This is done as control code textbox needs to lose focus
        self.driver.find_element_by_tag_name("body").click()

    def enter_control_code_unsure(self, code):
        control_code_tb = self.driver.find_element_by_id(self.UNSURE_CODE)
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def enter_control_unsure_details(self, details):
        unsure_details = self.driver.find_element_by_id(self.UNSURE_DETAILS)
        unsure_details.clear()
        unsure_details.send_keys(details)

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

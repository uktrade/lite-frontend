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
    ADD_A_GOOD_BTN = "add-a-good"  # ID

    # Add a good
    PART_NUMBER = "part_number"  # ID
    GOOD_IS_END_PRODUCT = "is_good_end_product-yes"  # ID
    GOOD_IS_NOT_END_PRODUCT = "is_good_end_product-no"  # ID
    CLC_CONFIRM = "clc_query_confirmation-"  # Partial ID
    IS_CONTROLLED = "is_good_controlled-"  # Partial ID
    CONTROL_CODE = "control_code"  # ID
    DESCRIPTION = "description"  # ID

    # Not sure form
    NOT_SURE_CODE = "not_sure_details_control_code"  # ID
    NOT_SURE_DETAILS = "not_sure_details_details"  # ID

    def click_add_a_good(self):
        self.driver.find_element_by_id(self.ADD_A_GOOD_BTN).click()

    def enter_description_of_goods(self, description, prefix=""):
        self.driver.find_element_by_id(prefix + self.DESCRIPTION).send_keys(description)

    def select_is_your_good_controlled(self, option, prefix=""):
        # The only options accepted here are 'yes', 'no' and 'unsure'
        self.driver.find_element_by_id(prefix + self.IS_CONTROLLED + option.lower()).click()

    def enter_control_code(self, code, prefix=""):
        control_code_tb = self.driver.find_element_by_id(prefix + self.CONTROL_CODE)
        control_code_tb.clear()
        control_code_tb.send_keys(code)

        # This is done as control code textbox needs to lose focus
        self.driver.find_element_by_tag_name("body").click()

    def enter_control_code_unsure(self, code, prefix=""):
        control_code_tb = self.driver.find_element_by_id(prefix + self.NOT_SURE_CODE)
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def enter_control_unsure_details(self, details):
        unsure_details = self.driver.find_element_by_id(self.NOT_SURE_DETAILS)
        unsure_details.clear()
        unsure_details.send_keys(details)

    def select_control_unsure_confirmation(self, option):
        # The only options accepted here are 'yes' and 'no
        self.driver.find_element_by_id(self.CLC_CONFIRM + option.lower()).click()

    def select_is_your_good_intended_to_be_incorporated_into_an_end_product(self, option, prefix=""):
        if option == "Yes":
            self.driver.find_element_by_id(prefix + self.GOOD_IS_NOT_END_PRODUCT).click()
        else:
            self.driver.find_element_by_id(prefix + self.GOOD_IS_END_PRODUCT).click()

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

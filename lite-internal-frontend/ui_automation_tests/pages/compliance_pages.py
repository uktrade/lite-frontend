from shared.BasePage import BasePage


class CompliancePages(BasePage):

    CASE_REFERENCE_ID = "reference"

    def find_case_reference(self, context):
        return self.driver.find_element_by_link_text(context.reference_code)

    def filter_by_case_reference(self, context):
        self.driver.find_element_by_id(self.CASE_REFERENCE_ID).send_keys(context.reference_code)

from helpers.BasePage import BasePage


class RecordDecision(BasePage):
    GRANT_LICENCE_RADIO = "status-approved"  # id
    DENY_LICENCE_RADIO = "status-declined"  # id
    OPTIONAL_TEXT = "reason_details"  # name
    DENIAL_REASONS_HEADER = ".govuk-heading-s"  # css
    DENIAL_REASONS_LISTED = ".govuk-label"  # css

    def click_on_grant_licence(self):
        self.driver.find_element_by_id(self.GRANT_LICENCE_RADIO).click()

    def click_on_deny_licence(self):
        self.driver.find_element_by_id(self.DENY_LICENCE_RADIO).click()

    def click_on_decision_number(self, no):
        self.driver.find_element_by_id(no).click()

    def enter_optional_text(self, text):
        self.driver.find_element_by_name(self.OPTIONAL_TEXT).send_keys(text)

    def get_text_of_denial_reasons_headers(self, no):
        return self.driver.find_elements_by_css_selector(self.DENIAL_REASONS_HEADER)[no].text

    def get_text_of_denial_reasons_listed(self, no):
        return self.driver.find_elements_by_css_selector(self.DENIAL_REASONS_LISTED)[no].text

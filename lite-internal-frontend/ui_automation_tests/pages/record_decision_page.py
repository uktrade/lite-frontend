class RecordDecision:
    def __init__(self, driver):
        self.driver = driver
        self.grant_licence_radio = "status-approved"  # id
        self.deny_licence_radio = "status-declined"  # id
        self.optional_text = "reason_details"  # name
        self.denial_reasons_header = ".govuk-heading-s"  # css
        self.denial_reasons_listed = ".govuk-label"  # css

    def click_on_grant_licence(self):
        self.driver.find_element_by_id(self.grant_licence_radio).click()

    def click_on_deny_licence(self):
        self.driver.find_element_by_id(self.deny_licence_radio).click()

    def click_on_decision_number(self, no):
        self.driver.find_element_by_id(no).click()

    def enter_optional_text(self, text):
        self.driver.find_element_by_name(self.optional_text).send_keys(text)

    def get_text_of_denial_reasons_headers(self, no):
        return self.driver.find_elements_by_css_selector(self.denial_reasons_header)[no].text

    def get_text_of_denial_reasons_listed(self, no):
        return self.driver.find_elements_by_css_selector(self.denial_reasons_listed)[no].text

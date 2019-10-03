class HMRCQueryPage:

    def __init__(self, driver):
        self.driver = driver

        self.govuk_input = '.govuk-input'
        self.govuk_radio_input = '.govuk-radios__input'

    def search_for_org(self, name):
        input = self.driver.find_element_by_css_selector(self.govuk_input)
        input.clear()
        input.send_keys(name)

    def select_first_org_in_list(self):
        self.driver.find_element_by_css_selector(self.govuk_radio_input).click()

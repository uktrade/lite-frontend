class Header:

    def __init__(self, driver):
        self.driver = driver
        self.application_name_in_header = ".lite-persistent-notice .govuk-link"

    def get_text_of_app_name_in_header(self):
        return self.driver.find_element_by_css_selector(self.application_name_in_header).text
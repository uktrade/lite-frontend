class Homepage():
    def __init__(self, driver):
        self.driver = driver
        self.error_message = driver.find_element_by_css_selector(".govuk-error-message")

    def get_text_of_error_message(self):
        return self.error_message.text

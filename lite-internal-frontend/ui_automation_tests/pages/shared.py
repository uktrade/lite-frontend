class Shared():

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "[type*='submit']" #css
        self.error_message = ".govuk-error-message" #css

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def get_text_of_error_message(self):
        return self.driver.find_element_by_css_selector(self.error_message).text

    def get_text_of_body(self):
        return self.driver.find_element_by_css_selector("body").text

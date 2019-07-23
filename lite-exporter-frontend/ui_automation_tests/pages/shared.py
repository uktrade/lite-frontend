class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = driver.find_element_by_css_selector("button[type*='submit']")
        self.submit_action_button = driver.find_element_by_css_selector("button[type*='submit']")
        self.error_message = driver.find_element_by_css_selector(".govuk-error-message")

    def get_text_of_error_message(self, position=0):
        return self.driver.find_elements_by_css_selector('.govuk-error-message')[position].text

    def click_save_and_continue(self):
        self.submit_button.click()

    def click_continue(self):
        self.submit_action_button.click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(".govuk-error-message").is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text


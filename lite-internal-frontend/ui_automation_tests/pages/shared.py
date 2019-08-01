class Shared():

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "[type*='submit']" #css
        self.error_message = ".govuk-error-message" #css

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def get_text_of_error_message(self, no):
        return self.driver.find_elements_by_css_selector(self.error_message)[no].text

    def get_text_of_body(self):
        return self.driver.find_element_by_css_selector("body").text

    def get_text_of_selected_tab(self):
        return self.driver.find_element_by_css_selector(".lite-tabs__tab.selected").text

    def get_text_of_table_body(self):
        return self.driver.find_element_by_css_selector(".govuk-table__body").text

    def get_text_of_caption(self):
        return self.driver.find_element_by_css_selector(".govuk-caption-l").text

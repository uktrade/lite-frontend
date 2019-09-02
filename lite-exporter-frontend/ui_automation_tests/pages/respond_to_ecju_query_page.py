from selenium.webdriver.common.keys import Keys


class RespondToEcjuQueryPage:

    def __init__(self, driver):
        self.driver = driver
        self.response_form = 'response'  # id

    def enter_form_response(self, value, ):
        response_tb = self.driver.find_element_by_id(self.response_form)
        response_tb.clear()
        response_tb.send_keys(value)

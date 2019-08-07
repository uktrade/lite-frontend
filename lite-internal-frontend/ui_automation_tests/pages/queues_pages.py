class QueuesPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_queue_text_field = "name" #id
        self.add_queue_button = ".govuk-button[href*='queues/add']" #css
        self.no_cases_text = '.lite-information-text__text' #css

    def enter_queue_name(self, text):
        self.driver.find_element_by_id(self.add_queue_text_field).clear()
        self.driver.find_element_by_id(self.add_queue_text_field).send_keys(text)

    def click_add_a_queue_button(self):
        self.driver.find_element_by_css_selector(self.add_queue_button).click()

    def case_is_on_the_list(self, app_id):
        self.driver.set_timeout_to(0)
        no = len(self.driver.find_elements_by_link_text(app_id))
        self.driver.set_timeout_to_10_seconds()

        return no

    def get_no_cases_text(self):
        return self.driver.find_element_by_css_selector(self.no_cases_text).text

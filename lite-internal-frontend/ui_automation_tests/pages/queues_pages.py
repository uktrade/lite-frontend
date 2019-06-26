class QueuesPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_queue_text_field = "name" #id
        self.add_queue_button = ".govuk-button[href*='queues/add']" #css

    def enter_queue_name(self, text):
        self.driver.find_element_by_id(self.add_queue_text_field).clear()
        self.driver.find_element_by_id(self.add_queue_text_field).send_keys(text)

    def click_add_a_queue_button(self):
        self.driver.find_element_by_css_selector(self.add_queue_button).click()

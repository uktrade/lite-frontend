class QueuesPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_queue_text_field = "name" #id
        self.add_queue_button = ".govuk-button[href*='queues/add']" #css
        self.caption_text = '.govuk-caption-l' #css

    def enter_queue_name(self, text):
        self.driver.find_element_by_id(self.add_queue_text_field).clear()
        self.driver.find_element_by_id(self.add_queue_text_field).send_keys(text)

    def click_add_a_queue_button(self):
        self.driver.find_element_by_css_selector(self.add_queue_button).click()

    def case_is_on_the_list(self, app_id):
        if self.driver.find_elements_by_link_text(app_id):
            return True
        else:
            return False

    def get_caption_text(self):
        return self.driver.find_element_by_css_selector(self.caption_text).text

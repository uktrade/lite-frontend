from selenium.webdriver.support.ui import Select


class FlagsPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_flag_text_field = "name" #id
        self.add_flag_button = ".govuk-button[href*='flags/add']" #css
        self.flags_in_edit_box = "lite-flag" #class_name

    def enter_flag_name(self, text):
        self.driver.find_element_by_id(self.add_flag_text_field).clear()
        self.driver.find_element_by_id(self.add_flag_text_field).send_keys(text)

    def select_flag_level(self, value):
        select = Select(self.driver.find_element_by_id('level'))
        select.select_by_visible_text(value)

    def click_add_a_flag_button(self):
        self.driver.find_element_by_css_selector(self.add_flag_button).click()

    def get_size_of_number_of_assigned_flags(self):
        return len(self.driver.find_elements_by_class_name(self.flags_in_edit_box))
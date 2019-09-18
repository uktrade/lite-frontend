from selenium.webdriver.common.keys import Keys


class AddEndUserPages:

    def __init__(self, driver):
        self.driver = driver
        self.add_new_address_button = 'a[href*="add"]'
        self.submit_button = "button[type*='submit']"
        self.type_choices = "sub_type-"
        self.back_to_overview_text = "Back to Application"  # link text

    def enter_name(self, name):
        name_tb = self.driver.find_element_by_id("name")
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_address(self, address):
        address_tb = self.driver.find_element_by_id("address")
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_website(self, website):
        address_tb = self.driver.find_element_by_id("website")
        address_tb.clear()
        address_tb.send_keys(website)

    def enter_country(self, country):
        country_tb = self.driver.find_element_by_id("country")
        country_tb.send_keys(country)

    def select_type(self, string):
        self.driver.find_element_by_id(self.type_choices + string).click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_continue(self):
        self.click_save_and_continue()

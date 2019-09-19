class AddNewExternalLocationFormPage:

    def __init__(self, driver):
        self.driver = driver
        self.add_new_address_button = 'a[href*="add"]'
        self.submit_button = "button[type*='submit']"

    def enter_external_location_name(self, name):
        name_tb = self.driver.find_element_by_id("name")
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_external_location_address(self, address):
        address_tb = self.driver.find_element_by_id("address")
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_external_location_country(self, country):
        country_tb = self.driver.find_element_by_id("country")
        country_tb.send_keys(country)

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_continue(self):
        self.click_save_and_continue()

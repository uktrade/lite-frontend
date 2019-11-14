class ExternalLocationsPage:

    def __init__(self, driver):
        self.driver = driver
        self.add_new_address_button = "//a[contains(@href, 'add')]"
        self.preexisting_locations_button = 'a[href*=preexisting'

    def click_add_new_address(self):
        self.driver.find_element_by_xpath(self.add_new_address_button).click()

    def click_preexisting_locations(self):
        self.driver.find_element_by_css_selector(self.preexisting_locations_button).click()

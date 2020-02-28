from ui_automation_tests.shared.BasePage import BasePage


class NewSite(BasePage):
    NAME = "name"
    ADDRESS_LINE_1 = "address.address_line_1"
    POSTCODE = "address.postcode"
    CITY = "address.city"
    REGION = "address.region"
    COUNTRY = "address.country"

    def enter_info_for_new_site(self, name, address, postcode, city, region, country):
        self.driver.find_element_by_id(self.COUNTRY).send_keys(country)
        self.driver.find_element_by_id(self.NAME).send_keys(name)
        self.driver.find_element_by_id(self.ADDRESS_LINE_1).send_keys(address)
        self.driver.find_element_by_id(self.POSTCODE).send_keys(postcode)
        self.driver.find_element_by_id(self.CITY).send_keys(city)
        self.driver.find_element_by_id(self.REGION).send_keys(region)

    def clear_info_for_site(self):
        self.driver.find_element_by_id(self.NAME).clear()
        self.driver.find_element_by_id(self.ADDRESS_LINE_1).clear()
        self.driver.find_element_by_id(self.POSTCODE).clear()
        self.driver.find_element_by_id(self.CITY).clear()
        self.driver.find_element_by_id(self.REGION).clear()

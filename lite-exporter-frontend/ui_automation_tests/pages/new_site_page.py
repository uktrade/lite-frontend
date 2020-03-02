from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class NewSite(BasePage):
    INPUT_NAME_ID = "name"
    INPUT_ADDRESS_LINE_1_ID = "address.address_line_1"
    INPUT_POSTCODE_ID = "address.postcode"
    INPUT_CITY_ID = "address.city"
    INPUT_REGION_ID = "address.region"
    AUTOCOMPLETE_COUNTRY_ID = "address.country"

    def enter_info_for_new_site(self, name, address, postcode, city, region, country):
        self.driver.find_element_by_id(self.INPUT_NAME_ID).send_keys(name)
        self.driver.find_element_by_id(self.INPUT_ADDRESS_LINE_1_ID).send_keys(address)
        self.driver.find_element_by_id(self.INPUT_CITY_ID).send_keys(city)
        self.driver.find_element_by_id(self.INPUT_REGION_ID).send_keys(region)
        self.driver.find_element_by_id(self.INPUT_POSTCODE_ID).send_keys(postcode)
        functions.send_keys_to_autocomplete(self.driver, self.AUTOCOMPLETE_COUNTRY_ID, country)

    def clear_info_for_site(self):
        self.driver.find_element_by_id(self.INPUT_NAME_ID).clear()
        self.driver.find_element_by_id(self.INPUT_ADDRESS_LINE_1_ID).clear()
        self.driver.find_element_by_id(self.INPUT_POSTCODE_ID).clear()
        self.driver.find_element_by_id(self.INPUT_CITY_ID).clear()
        self.driver.find_element_by_id(self.INPUT_REGION_ID).clear()
        self.driver.find_element_by_id(self.AUTOCOMPLETE_COUNTRY_ID).clear()

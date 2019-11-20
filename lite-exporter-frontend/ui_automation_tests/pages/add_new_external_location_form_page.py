from shared.BasePage import BasePage


class AddNewExternalLocationFormPage(BasePage):

    ADD_NEW_ADDRESS_BUTTON = 'a[href*="add"]'

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

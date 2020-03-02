from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


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
        functions.send_keys_to_autocomplete(self.driver, "country", country)

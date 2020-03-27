from ui_automation_tests.shared.BasePage import BasePage


class NewSite(BasePage):
    RADIOBUTTON_IN_THE_UNITED_KINGDOM_ID = "location-united_kingdom"
    INPUT_NAME_ID = "name"
    INPUT_ADDRESS_LINE_1_ID = "address.address_line_1"
    INPUT_POSTCODE_ID = "address.postcode"
    INPUT_CITY_ID = "address.city"
    INPUT_REGION_ID = "address.region"

    def click_in_the_united_kingdom_radiobutton(self):
        self.driver.find_element_by_id(self.RADIOBUTTON_IN_THE_UNITED_KINGDOM_ID).click()

    def enter_new_site_details(self, name, address, postcode, city, region):
        self.driver.find_element_by_id(self.INPUT_NAME_ID).send_keys(name)
        self.driver.find_element_by_id(self.INPUT_ADDRESS_LINE_1_ID).send_keys(address)
        self.driver.find_element_by_id(self.INPUT_CITY_ID).send_keys(city)
        self.driver.find_element_by_id(self.INPUT_REGION_ID).send_keys(region)
        self.driver.find_element_by_id(self.INPUT_POSTCODE_ID).send_keys(postcode)

    def change_site_name(self, name):
        self.driver.find_element_by_id(self.INPUT_NAME_ID).clear()
        self.driver.find_element_by_id(self.INPUT_NAME_ID).send_keys(name)

    def click_all_users(self):
        checkboxes = self.driver.find_elements_by_class_name("govuk-checkboxes__label")
        for checkbox in checkboxes:
            checkbox.click()

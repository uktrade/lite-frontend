from ui_automation_tests.shared.BasePage import BasePage
from ui_automation_tests.shared import functions


class AddEndUserPages(BasePage):
    INPUT_NAME_ID = "name"
    INPUT_ADDRESS_ID = "address"
    INPUT_COUNTRY_ID = "country"
    INPUT_WEBSITE_ID = "website"

    LINK_SHOW_FILTER_ID = "show-filters-link"
    INPUT_FILTER_NAME_ID = "name"
    INPUT_FILTER_ADDRESS_ID = "address"
    INPUT_FILTER_COUNTRY_ID = "country"
    BUTTON_SUBMIT_FILTER_ID = "button-apply-filters"

    INPUT_PARTY_TYPE_ID_PARTIAL = "sub_type-"
    INPUT_PARTY_TYPE_NAME = "sub_type"
    INPUT_CREATE_NEW_OR_COPY_ID = "copy_existing"
    LINK_COPY_EXISTING_ID = "copy"

    def create_new_or_copy_existing(self, copy_existing: bool):
        if copy_existing:
            self.driver.find_element_by_id(f"{self.INPUT_CREATE_NEW_OR_COPY_ID}-yes").click()
        else:
            self.driver.find_element_by_id(f"{self.INPUT_CREATE_NEW_OR_COPY_ID}-no").click()
        functions.click_submit(self.driver)

    def enter_name(self, name):
        name_tb = self.driver.find_element_by_id(self.INPUT_NAME_ID)
        name_tb.clear()
        name_tb.send_keys(name)

    def get_name(self):
        return self.driver.find_element_by_id(self.INPUT_NAME_ID).get_attribute("value")

    def enter_address(self, address):
        address_tb = self.driver.find_element_by_id(self.INPUT_ADDRESS_ID)
        address_tb.clear()
        address_tb.send_keys(address)

    def get_address(self):
        return self.driver.find_element_by_id(self.INPUT_ADDRESS_ID).get_attribute("value")

    def enter_website(self, website):
        address_tb = self.driver.find_element_by_id(self.INPUT_WEBSITE_ID)
        address_tb.clear()
        address_tb.send_keys(website)

    def get_website(self):
        return self.driver.find_element_by_id(self.INPUT_WEBSITE_ID).get_attribute("value")

    def enter_country(self, country):
        functions.send_keys_to_autocomplete(self.driver, self.INPUT_COUNTRY_ID, country)

    def get_country(self):
        return self.driver.find_element_by_id(self.INPUT_COUNTRY_ID).get_attribute("value")

    def select_type(self, string):
        self.driver.find_element_by_id(self.INPUT_PARTY_TYPE_ID_PARTIAL + string).click()

    def get_type(self):
        for option in self.driver.find_elements_by_name(self.INPUT_PARTY_TYPE_NAME):
            if option.get_attribute("selected") == "true":
                return option.get_attribute("value")
        return None

    def click_copy_existing_button(self):
        self.driver.find_element_by_id(self.LINK_COPY_EXISTING_ID).click()

    def open_parties_filter(self):
        self.driver.find_element_by_id(self.LINK_SHOW_FILTER_ID).click()

    def filter_name(self, text):
        self.driver.find_element_by_id(self.INPUT_FILTER_NAME_ID).send_keys(text)

    def filter_address(self, text):
        self.driver.find_element_by_id(self.INPUT_FILTER_ADDRESS_ID).send_keys(text)

    def filter_country(self, text):
        self.driver.find_element_by_id(self.INPUT_FILTER_COUNTRY_ID).send_keys(text)

    def submit_filter(self):
        self.driver.find_element_by_id(self.BUTTON_SUBMIT_FILTER_ID).click()

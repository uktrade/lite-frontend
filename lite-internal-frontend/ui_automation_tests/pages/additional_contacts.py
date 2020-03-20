from shared import functions
from shared.BasePage import BasePage


class AdditionalContactsPage(BasePage):

    BUTTON_ADD_A_CONTACT_ID = "button-add-a-contact"
    INPUT_DETAILS_ID = "details"
    INPUT_NAME_ID = "name"
    INPUT_ADDRESS_ID = "address"
    AUTOCOMPLETE_COUNTRY_ID = "country"
    INPUT_EMAIL_ID = "email"
    INPUT_PHONE_NUMBER_ID = "phone_number"

    def enter_details(self, text):
        self.driver.find_element_by_id(self.INPUT_DETAILS_ID).send_keys(text)

    def enter_name(self, text):
        self.driver.find_element_by_id(self.INPUT_NAME_ID).send_keys(text)

    def enter_address(self, text):
        self.driver.find_element_by_id(self.INPUT_ADDRESS_ID).send_keys(text)

    def enter_country(self, text):
        functions.send_keys_to_autocomplete(self.driver, self.AUTOCOMPLETE_COUNTRY_ID, text)

    def enter_email(self, text):
        self.driver.find_element_by_id(self.INPUT_EMAIL_ID).send_keys(text)

    def enter_phone_number(self, text):
        self.driver.find_element_by_id(self.INPUT_PHONE_NUMBER_ID).send_keys(text)

    def click_add_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_CONTACT_ID).click()

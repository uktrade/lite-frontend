from faker import Faker

from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage

fake = Faker()


class OpenApplicationCountryContractTypes(BasePage):
    RADIOBUTTON_ALL_COUNTRIES = "choice-all"

    OTHER_CONTRACT_TYPE_CHECKBOX_ID = "Other---specify-below"
    OTHER_CONTRACT_TYPE_INPUT_ID = "other_contract_type_text"

    def select_same_contract_types_for_all_countries_radio_button(self):
        self.driver.find_element_by_id(self.RADIOBUTTON_ALL_COUNTRIES).click()
        functions.click_submit(self.driver)

    def select_contract_type(self, contract_type_id):
        self.driver.find_element_by_id(contract_type_id).click()

    def select_other_contract_type_and_fill_in_details(self):
        other_contract_type = fake.sentence(nb_words=5)
        self.driver.find_element_by_id(self.OTHER_CONTRACT_TYPE_CHECKBOX_ID).click()
        details_element = self.driver.find_element_by_id(self.OTHER_CONTRACT_TYPE_INPUT_ID)
        details_element.clear()
        details_element.send_keys(other_contract_type)

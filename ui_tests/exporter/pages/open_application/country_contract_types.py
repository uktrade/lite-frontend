from faker import Faker

from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.exporter.pages.BasePage import BasePage

fake = Faker()


class OpenApplicationCountryContractTypes(BasePage):
    RADIOBUTTON_ALL_COUNTRIES = "choice-all"

    OTHER_CONTRACT_TYPE_CHECKBOX_ID = "Other---specify-below"
    OTHER_CONTRACT_TYPE_INPUT_ID = "other_contract_type_text"

    def select_same_contract_types_for_all_countries_radio_button(self):
        self.driver.find_element(by=By.ID, value=self.RADIOBUTTON_ALL_COUNTRIES).click()
        functions.click_submit(self.driver)

    def select_contract_type(self, contract_type_id):
        self.driver.find_element(by=By.ID, value=contract_type_id).click()

    def select_other_contract_type_and_fill_in_details(self):
        other_contract_type = fake.sentence(nb_words=5)
        self.driver.find_element(by=By.ID, value=self.OTHER_CONTRACT_TYPE_CHECKBOX_ID).click()
        details_element = self.driver.find_element(by=By.ID, value=self.OTHER_CONTRACT_TYPE_INPUT_ID)
        details_element.clear()
        details_element.send_keys(other_contract_type)

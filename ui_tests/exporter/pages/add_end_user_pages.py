from selenium.webdriver.common.by import By
from ui_tests.exporter.pages.BasePage import BasePage
from tests_common import functions


class AddEndUserPages(BasePage):
    INPUT_NAME_ID = "name"
    INPUT_ADDRESS_ID = "address"
    INPUT_COUNTRY_ID = "country-autocomplete"
    INPUT_WEBSITE_ID = "website"
    INPUT_SIGNATORY_NAME_ID = "signatory_name_euu"

    LINK_SHOW_FILTER_ID = "show-filters-link"
    INPUT_FILTER_NAME_ID = "name"
    INPUT_FILTER_ADDRESS_ID = "address"
    INPUT_FILTER_COUNTRY_ID = "country"
    BUTTON_SUBMIT_FILTER_ID = "button-apply-filters"

    INPUT_CREATE_NEW_OR_COPY_ID = "copy_existing"
    LINK_COPY_EXISTING_ID = "copy"

    def create_new_or_copy_existing(self, copy_existing: bool):
        if copy_existing:
            self.driver.find_element(by=By.ID, value=f"{self.INPUT_CREATE_NEW_OR_COPY_ID}-yes").click()
        else:
            self.driver.find_element(by=By.ID, value=f"{self.INPUT_CREATE_NEW_OR_COPY_ID}-no").click()
        functions.click_submit(self.driver)

    def enter_name(self, name):
        name_tb = self.driver.find_element(by=By.XPATH, value=f"//input[contains(@id, '{self.INPUT_NAME_ID}')]")
        name_tb.clear()
        name_tb.send_keys(name)

    def get_name(self):
        return self.driver.find_element(by=By.ID, value=self.INPUT_NAME_ID).get_attribute("value")

    def enter_address(self, address):
        address_tb = self.driver.find_element(
            by=By.XPATH, value=f"//textarea[contains(@id, '{self.INPUT_ADDRESS_ID}')]"
        )
        address_tb.clear()
        address_tb.send_keys(address)

    def get_address(self):
        return self.driver.find_element(by=By.ID, value=self.INPUT_ADDRESS_ID).get_attribute("value")

    def enter_website(self, website):
        address_tb = self.driver.find_element(by=By.ID, value=self.INPUT_WEBSITE_ID)
        address_tb.clear()
        address_tb.send_keys(website)

    def get_website(self):
        return self.driver.find_element(by=By.ID, value=self.INPUT_WEBSITE_ID).get_attribute("value")

    def enter_country(self, country):
        functions.send_keys_to_autocomplete(self.driver, self.INPUT_COUNTRY_ID, country)

    def get_country(self):
        return self.driver.find_element(by=By.ID, value=self.INPUT_COUNTRY_ID).get_attribute("value")

    def select_type(self, option):
        self.driver.find_element(by=By.CSS_SELECTOR, value=f"*[value='{option.lower()}']").click()

    def click_copy_existing_button(self):
        self.driver.find_element(by=By.ID, value=self.LINK_COPY_EXISTING_ID).click()

    def open_parties_filter(self):
        self.driver.find_element(by=By.ID, value=self.LINK_SHOW_FILTER_ID).click()

    def filter_name(self, text):
        self.driver.find_element(by=By.ID, value=self.INPUT_FILTER_NAME_ID).send_keys(text)

    def filter_address(self, text):
        self.driver.find_element(by=By.ID, value=self.INPUT_FILTER_ADDRESS_ID).send_keys(text)

    def filter_country(self, text):
        self.driver.find_element(by=By.ID, value=self.INPUT_FILTER_COUNTRY_ID).send_keys(text)

    def submit_filter(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_SUBMIT_FILTER_ID).click()

    def choose_reuse_existing_party(self, option):
        self.driver.find_element(by=By.CSS_SELECTOR, value=f"*[value='{option.lower()}']").click()

    def enter_signatory_name(self, name):
        self.driver.find_element(
            by=By.XPATH, value=f"//input[contains(@id, '{self.INPUT_SIGNATORY_NAME_ID}')]"
        ).send_keys(name)

    def enter_no_end_user_document_reason(self, reason):
        self.driver.find_element(by=By.TAG_NAME, value="textarea").send_keys(reason)

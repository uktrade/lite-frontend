from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.functions import element_with_css_selector_exists


class AddEndUserAdvisoryPages(BasePage):

    ADD_NEW_ADDRESS_BUTTON = 'a[href*="add"]'
    TYPE_CHOICES = "sub_type-"

    NATURE_OF_BUSINESS = "nature_of_business"  # ID
    PRIMARY_CONTACT_EMAIL = "contact_email"  # ID
    PRIMARY_CONTACT_NAME = "contact_name"  # ID
    PRIMARY_CONTACT_TELEPHONE = "contact_telephone"  # ID
    PRIMARY_CONTACT_JOB_TITLE = "contact_job_title"  # ID

    DETAIL_BODY_CSS_SELECTOR = ".govuk-panel__body"
    SUCCESS_PANEL_CSS_SELECTOR = ".govuk-panel--confirmation"

    def enter_name(self, name, prefix=""):
        name_tb = self.driver.find_element(by=By.ID, value=prefix + "name")
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_address(self, address, prefix=""):
        address_tb = self.driver.find_element(by=By.ID, value=prefix + "address")
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_website(self, website, prefix=""):
        address_tb = self.driver.find_element(by=By.ID, value=prefix + "website")
        address_tb.clear()
        address_tb.send_keys(website)

    def enter_country(self, country, prefix=""):
        functions.send_keys_to_autocomplete(self.driver, prefix + "country", country)

    def enter_reasoning(self, reasoning):
        reasoning_tb = self.driver.find_element(by=By.ID, value="reasoning")
        reasoning_tb.send_keys(reasoning)

    def enter_notes(self, notes):
        reasoning_tb = self.driver.find_element(by=By.ID, value="note")
        reasoning_tb.send_keys(notes)

    def select_type(self, string, prefix=""):
        self.driver.find_element(by=By.ID, value=prefix + self.TYPE_CHOICES + string).click()

    def enter_nature(self, nature_of_business):
        nature_of_business_tb = self.driver.find_element(by=By.ID, value=self.NATURE_OF_BUSINESS)
        nature_of_business_tb.send_keys(nature_of_business)

    def enter_primary_contact_email(self, primary_contact_email):
        primary_contact_email_tb = self.driver.find_element(by=By.ID, value=self.PRIMARY_CONTACT_EMAIL)
        primary_contact_email_tb.send_keys(primary_contact_email)

    def enter_primary_contact_name(self, primary_contact_name):
        primary_contact_name_tb = self.driver.find_element(by=By.ID, value=self.PRIMARY_CONTACT_NAME)
        primary_contact_name_tb.send_keys(primary_contact_name)

    def enter_primary_contact_job_title(self, primary_contact_job_title):
        primary_contact_name_tb = self.driver.find_element(by=By.ID, value=self.PRIMARY_CONTACT_JOB_TITLE)
        primary_contact_name_tb.send_keys(primary_contact_job_title)

    def enter_primary_contact_telephone(self, primary_contact_telephone):
        primary_contact_telephone_tb = self.driver.find_element(by=By.ID, value=self.PRIMARY_CONTACT_TELEPHONE)
        primary_contact_telephone_tb.send_keys(primary_contact_telephone)

    def get_ecju_reference_from_success_banner(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.DETAIL_BODY_CSS_SELECTOR).text.split(": ")[1]

    def success_panel_is_present(self):
        return element_with_css_selector_exists(self.driver, self.SUCCESS_PANEL_CSS_SELECTOR)

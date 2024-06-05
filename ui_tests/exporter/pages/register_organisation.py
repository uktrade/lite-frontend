from random import randint

from selenium.webdriver.common.by import By

from faker import Faker
from faker.providers.phone_number import Provider

from tests_common import functions
from ui_tests.exporter.pages.BasePage import BasePage


class UKPhoneNumberProvider(Provider):
    def uk_phone_number(self):
        return "+441234567890"


fake = Faker("en_GB")
fake.add_provider(UKPhoneNumberProvider)


class RegisterOrganisation(BasePage):
    CREATE_ACCOUNT_ID = "button-Create an account"
    COMMERCIAL_INDIVIDUAL_PARTIAL_ID = "type-"
    INDIVIDUAL_RADIO_ID = "type-individual"
    COMPANY_NAME_ID = "id_REGISTRATION_DETAILS-name"
    EORI_ID = "id_REGISTRATION_DETAILS-eori_number"
    SIC_ID = "id_REGISTRATION_DETAILS-sic_number"
    VAT_ID = "id_REGISTRATION_DETAILS-vat_number"
    REG_ID = "id_REGISTRATION_DETAILS-registration_number"
    SITE_NAME_ID = "id_ADDRESS_DETAILS-name"
    SITE_ADDRESS_LINE_1_ID = "id_ADDRESS_DETAILS-address_line_1"
    SITE_ADDRESS = "site.address.address"
    SITE_CITY_ID = "id_ADDRESS_DETAILS-city"
    SITE_REGION_ID = "id_ADDRESS_DETAILS-region"
    SITE_POSTCODE_ID = "id_ADDRESS_DETAILS-postcode"
    SITE_COUNTRY_ID = "site.address.country"
    SITE_PHONE_NUMBER_ID = "id_ADDRESS_DETAILS-phone_number"
    OUTSIDE_OF_UK_RADIO_ID = "location-abroad"
    INSIDE_OF_UK_RADIO_ID = "location-united_kingdom"

    def click_create_an_account_button(self):
        self.driver.find_element(by=By.ID, value=self.CREATE_ACCOUNT_ID).click()

    def select_commercial_or_individual_organisation(self, selection):
        self.driver.find_element(by=By.ID, value=self.COMMERCIAL_INDIVIDUAL_PARTIAL_ID + selection).click()

    def enter_random_company_name(self):
        self.driver.find_element(by=By.ID, value=self.COMPANY_NAME_ID).send_keys(fake.company())

    def click_outside_of_uk_location(self):
        self.driver.find_element(by=By.ID, value=self.OUTSIDE_OF_UK_RADIO_ID).click()

    def click_inside_of_uk_location(self):
        self.driver.find_element(by=By.ID, value=self.INSIDE_OF_UK_RADIO_ID).click()

    def enter_random_eori_number(self, eori_number):
        self.driver.find_element(by=By.ID, value=self.EORI_ID).send_keys(eori_number)

    def enter_random_sic_number(self):
        self.driver.find_element(by=By.ID, value=self.SIC_ID).send_keys(randint(10000, 99999))

    def enter_random_vat_number(self):
        self.driver.find_element(by=By.ID, value=self.VAT_ID).send_keys("GB" + str(randint(100000000, 999999999)))

    def enter_random_registration_number(self):
        self.driver.find_element(by=By.ID, value=self.REG_ID).send_keys(randint(10000000, 99999999))

    def enter_random_site(self):
        self.driver.find_element(by=By.ID, value=self.SITE_NAME_ID).send_keys(fake.secondary_address())
        self.driver.find_element(by=By.ID, value=self.SITE_ADDRESS_LINE_1_ID).send_keys(fake.street_address())
        self.driver.find_element(by=By.ID, value=self.SITE_CITY_ID).send_keys(fake.city())
        self.driver.find_element(by=By.ID, value=self.SITE_REGION_ID).send_keys(fake.county())
        self.driver.find_element(by=By.ID, value=self.SITE_POSTCODE_ID).send_keys(fake.postcode())
        self.driver.find_element(by=By.ID, value=self.SITE_PHONE_NUMBER_ID).send_keys(fake.uk_phone_number())

    def enter_random_site_with_country_and_address_box(self):
        self.driver.find_element(by=By.ID, value=self.SITE_NAME_ID).send_keys(fake.secondary_address())
        self.driver.find_element(by=By.ID, value=self.SITE_ADDRESS).send_keys(fake.street_address())
        self.driver.find_element(by=By.ID, value=self.SITE_ADDRESS).send_keys(fake.city())
        self.driver.find_element(by=By.ID, value=self.SITE_ADDRESS).send_keys(fake.state())
        self.driver.find_element(by=By.ID, value=self.SITE_ADDRESS).send_keys(fake.postcode())
        functions.send_keys_to_autocomplete(self.driver, self.SITE_COUNTRY_ID, "Canada")

from random import randint

from faker import Faker

from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage

fake = Faker()


class RegisterOrganisation(BasePage):
    CREATE_ACCOUNT_ID = "button-Create an account"
    COMMERCIAL_INDIVIDUAL_PARTIAL_ID = "type-"
    INDIVIDUAL_RADIO_ID = "type-individual"
    COMPANY_NAME_ID = "name"
    EORI_ID = "eori_number"
    SIC_ID = "sic_number"
    VAT_ID = "vat_number"
    REG_ID = "registration_number"
    SITE_NAME_ID = "site.name"
    SITE_ADDRESS_LINE_1_ID = "site.address.address_line_1"
    SITE_ADDRESS = "site.address.address"
    SITE_CITY_ID = "site.address.city"
    SITE_REGION_ID = "site.address.region"
    SITE_POSTCODE_ID = "site.address.postcode"
    SITE_COUNTRY_ID = "site.address.country"
    OUTSIDE_OF_UK_RADIO_ID = "location-abroad"
    INSIDE_OF_UK_RADIO_ID = "location-united_kingdom"

    def click_create_an_account_button(self):
        self.driver.find_element_by_id(self.CREATE_ACCOUNT_ID).click()

    def select_commercial_or_individual_organisation(self, selection):
        self.driver.find_element_by_id(self.COMMERCIAL_INDIVIDUAL_PARTIAL_ID + selection).click()

    def enter_random_company_name(self):
        self.driver.find_element_by_id(self.COMPANY_NAME_ID).send_keys(fake.company())

    def click_outside_of_uk_location(self):
        self.driver.find_element_by_id(self.OUTSIDE_OF_UK_RADIO_ID).click()

    def click_inside_of_uk_location(self):
        self.driver.find_element_by_id(self.INSIDE_OF_UK_RADIO_ID).click()

    def enter_random_eori_number(self):
        self.driver.find_element_by_id(self.EORI_ID).send_keys(randint(10000, 99999))

    def enter_random_sic_number(self):
        self.driver.find_element_by_id(self.SIC_ID).send_keys(randint(10000, 99999))

    def enter_random_vat_number(self):
        self.driver.find_element_by_id(self.VAT_ID).send_keys("GB" + str(randint(100000000, 999999999)))

    def enter_random_registration_number(self):
        self.driver.find_element_by_id(self.REG_ID).send_keys(randint(10000000, 99999999))

    def enter_random_site(self):
        self.driver.find_element_by_id(self.SITE_NAME_ID).send_keys(fake.secondary_address())
        self.driver.find_element_by_id(self.SITE_ADDRESS_LINE_1_ID).send_keys(fake.street_address())
        self.driver.find_element_by_id(self.SITE_CITY_ID).send_keys(fake.city())
        self.driver.find_element_by_id(self.SITE_REGION_ID).send_keys(fake.state())
        self.driver.find_element_by_id(self.SITE_POSTCODE_ID).send_keys(fake.postcode())

    def enter_random_site_with_country_and_address_box(self):
        self.driver.find_element_by_id(self.SITE_NAME_ID).send_keys(fake.secondary_address())
        self.driver.find_element_by_id(self.SITE_ADDRESS).send_keys(fake.street_address())
        self.driver.find_element_by_id(self.SITE_ADDRESS).send_keys(fake.city())
        self.driver.find_element_by_id(self.SITE_ADDRESS).send_keys(fake.state())
        self.driver.find_element_by_id(self.SITE_ADDRESS).send_keys(fake.postcode())
        functions.send_keys_to_autocomplete(self.driver, self.SITE_COUNTRY_ID, "Canada")

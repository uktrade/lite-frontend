from selenium.webdriver.common.by import By

from faker import Faker

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage

fake = Faker()


class OrganisationsFormPage(BasePage):
    def click_new_organisation_btn(self):
        new_organisation_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="a[href*='organisations/register']")
        new_organisation_btn.click()

    def select_type(self, individual_or_commercial):
        self.driver.find_element(by=By.ID, value="type-" + individual_or_commercial).click()
        functions.click_submit(self.driver)

    def select_location(self, united_kingdom_or_abroad):
        self.driver.find_element(by=By.ID, value="location-" + united_kingdom_or_abroad).click()
        functions.click_submit(self.driver)

    def enter_name(self, text):
        name = self.driver.find_element(by=By.ID, value="name")
        name.clear()
        name.send_keys(text)

    def enter_eori_number(self, text):
        eori_number = self.driver.find_element(by=By.ID, value="eori_number")
        eori_number.clear()
        eori_number.send_keys(text)

    def enter_sic_number(self, text):
        sic_number = self.driver.find_element(by=By.ID, value="sic_number")
        sic_number.clear()
        sic_number.send_keys(text)

    def enter_vat_number(self, text):
        vat_number = self.driver.find_element(by=By.ID, value="vat_number")
        vat_number.clear()
        vat_number.send_keys(text)

    def enter_registration_number(self, text):
        registration_number = self.driver.find_element(by=By.ID, value="registration_number")
        registration_number.clear()
        registration_number.send_keys(text)

    def enter_site_name(self, text):
        site_name = self.driver.find_element(by=By.ID, value="site.name")
        site_name.clear()
        site_name.send_keys(text)

    def enter_address_line_1(self, text):
        site_address_line_1 = self.driver.find_element(by=By.ID, value="site.address.address_line_1")
        site_address_line_1.clear()
        site_address_line_1.send_keys(text)

    def enter_address(self, text):
        address = self.driver.find_element(by=By.ID, value="site.address.address")
        address.clear()
        address.send_keys(text)

    def enter_post_code(self, text):
        site_address_postcode = self.driver.find_element(by=By.ID, value="site.address.postcode")
        site_address_postcode.clear()
        site_address_postcode.send_keys(text)

    def enter_city(self, text):
        site_address_city = self.driver.find_element(by=By.ID, value="site.address.city")
        site_address_city.clear()
        site_address_city.send_keys(text)

    def enter_region(self, text):
        site_address_region = self.driver.find_element(by=By.ID, value="site.address.region")
        site_address_region.clear()
        site_address_region.send_keys(text)

    def enter_country(self, text):
        functions.send_keys_to_autocomplete(self.driver, "site.address.country", text)

    def enter_individual_organisation_first_last_name(self, text):
        self.driver.find_element(by=By.ID, value="name").send_keys(text)

    def enter_email(self, text):
        self.driver.find_element(by=By.ID, value="user.email").send_keys(text)
        functions.click_submit(self.driver)

    def fill_in_company_info_page_1(self, context):
        if hasattr(context, "organisation_name"):
            context.old_organisation_name = context.organisation_name
        context.organisation_name = fake.company() + " " + fake.company_suffix()
        self.enter_name(context.organisation_name)
        context.eori = "12345"
        self.enter_eori_number(context.eori)
        context.sic = "12345"
        self.enter_sic_number(context.sic)
        context.vat = "GB123456789"
        self.enter_vat_number(context.vat)
        self.enter_registration_number(12345678)
        functions.click_submit(self.driver)

    def fill_in_individual_info_page_1(self, context):
        context.organisation_name = fake.name()
        context.eori = "12345"
        self.enter_individual_organisation_first_last_name(context.organisation_name)
        self.enter_email(fake.free_email())
        functions.click_submit(self.driver)

    def enter_site_details(self, context, location):
        context.site_name = fake.company()
        self.enter_site_name(context.site_name)
        if location == "united_kingdom":
            self.enter_address_line_1(fake.street_address())
            self.enter_region(fake.city())
            self.enter_post_code(fake.postcode())
            self.enter_city(fake.state())
        else:
            self.enter_address(fake.street_address())
            self.enter_country("Ukraine")
        functions.click_submit(self.driver)

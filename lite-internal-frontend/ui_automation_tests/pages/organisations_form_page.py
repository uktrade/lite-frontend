from shared.BasePage import BasePage


class OrganisationsFormPage(BasePage):
    def click_new_organisation_btn(self):
        new_organisation_btn = self.driver.find_element_by_css_selector("a[href*='organisations/register']")
        new_organisation_btn.click()

    def select_type(self, individual_or_commercial):
        self.driver.find_element_by_id("type-" + individual_or_commercial).click()

    def enter_name(self, text):
        name = self.driver.find_element_by_id("name")
        name.clear()
        name.send_keys(text)

    def enter_eori_number(self, text):
        eori_number = self.driver.find_element_by_id("eori_number")
        eori_number.clear()
        eori_number.send_keys(text)

    def enter_sic_number(self, text):
        sic_number = self.driver.find_element_by_id("sic_number")
        sic_number.clear()
        sic_number.send_keys(text)

    def enter_vat_number(self, text):
        vat_number = self.driver.find_element_by_id("vat_number")
        vat_number.clear()
        vat_number.send_keys(text)

    def enter_registration_number(self, text):
        registration_number = self.driver.find_element_by_id("registration_number")
        registration_number.clear()
        registration_number.send_keys(text)

    def enter_site_name(self, text):
        site_name = self.driver.find_element_by_id("site.name")
        site_name.clear()
        site_name.send_keys(text)

    def enter_address_line_1(self, text):
        site_address_line_1 = self.driver.find_element_by_id("site.address.address_line_1")
        site_address_line_1.clear()
        site_address_line_1.send_keys(text)

    def enter_post_code(self, text):
        site_address_postcode = self.driver.find_element_by_id("site.address.postcode")
        site_address_postcode.clear()
        site_address_postcode.send_keys(text)

    def enter_city(self, text):
        site_address_city = self.driver.find_element_by_id("site.address.city")
        site_address_city.clear()
        site_address_city.send_keys(text)

    def enter_region(self, text):
        site_address_region = self.driver.find_element_by_id("site.address.region")
        site_address_region.clear()
        site_address_region.send_keys(text)

    def enter_country(self, text):
        country_tb = self.driver.find_element_by_id("site.address.country")
        country_tb.send_keys(text)

    def enter_individual_organisation_first_last_name(self, text):
        self.driver.find_element_by_id("name").send_keys(text)

    def enter_email(self, text):
        self.driver.find_element_by_id("user.email").send_keys(text)

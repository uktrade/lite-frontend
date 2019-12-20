from shared.BasePage import BasePage


class OrganisationsFormPage(BasePage):
    def click_new_organisation_btn(self):
        new_organisation_btn = self.driver.find_element_by_css_selector("a[href*='organisations/register']")
        new_organisation_btn.click()

    def select_type(self, individual_or_commercial):
        self.driver.find_element_by_id("type-" + individual_or_commercial).click()

    def enter_name(self, text):
        self.driver.find_element_by_id("name").send_keys(text)

    def enter_eori_number(self, text):
        self.driver.find_element_by_id("eori_number").send_keys(text)

    def enter_sic_number(self, text):
        self.driver.find_element_by_id("sic_number").send_keys(text)

    def enter_vat_number(self, text):
        self.driver.find_element_by_id("vat_number").send_keys(text)

    def enter_registration_number(self, text):
        self.driver.find_element_by_id("registration_number").send_keys(text)

    def enter_site_name(self, text):
        self.driver.find_element_by_id("site.name").send_keys(text)

    def enter_address_line_1(self, text):
        self.driver.find_element_by_id("site.address.address_line_1").send_keys(text)

    def enter_post_code(self, text):
        self.driver.find_element_by_id("site.address.postcode").send_keys(text)

    def enter_city(self, text):
        self.driver.find_element_by_id("site.address.city").send_keys(text)

    def enter_region(self, text):
        self.driver.find_element_by_id("site.address.region").send_keys(text)

    def enter_country(self, text):
        country_tb = self.driver.find_element_by_id("site.address.country")
        country_tb.send_keys(text)

    def enter_individual_organisation_first_last_name(self, text):
        self.driver.find_element_by_id("name").send_keys(text)

    def enter_email(self, text):
        self.driver.find_element_by_id("user.email").send_keys(text)

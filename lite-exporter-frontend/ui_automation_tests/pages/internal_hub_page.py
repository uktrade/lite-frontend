from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import time

class InternalHubPage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.queue_drop_down = "a[href*='/apply_for_a_licence/']"
        self.go_to_queue_btn = "button.govuk-button"

    def select_from_queue_drop_down(self, value):
        select = Select(self.find_element_by_name('queue'))
        select.select_by_visible_text(value)

    def click_go_to_queue_button(self):
        self.driver.find_element_by_css_selector(self.go_to_queue_btn).click()

    def enter_business_name(self, business_name):
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys(business_name)

    def enter_eori_number(self, eori_number):
        self.driver.find_element_by_id("eori_number").clear()
        self.driver.find_element_by_id("eori_number").send_keys(eori_number)

    def enter_sic_number(self, sic_number):
        self.driver.find_element_by_id("sic_number").clear()
        self.driver.find_element_by_id("sic_number").send_keys(sic_number)

    def enter_vat_number(self,vat_number):
        self.driver.find_element_by_id("vat_number").clear()
        self.driver.find_element_by_id("vat_number").send_keys(vat_number)

    def enter_company_registration_number(self, registration_number):
        self.driver.find_element_by_id("registration_number").clear()
        self.driver.find_element_by_id("registration_number").send_keys(registration_number)

    def enter_address(self, address):
        self.driver.find_element_by_id("address").clear()
        self.driver.find_element_by_id("address").send_keys(address)

    def enter_admin_user_email(self, email):
        self.driver.find_element_by_id("admin_user_email").click()
        self.driver.find_element_by_id("admin_user_email").send_keys(email)

    def click_submit(self):
        submit = self.driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

    def click_save_and_continue(self):
        submit = self.driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

    def click_cancel(self):
        cancel_btn = self.driver.find_element_by_css_selector("a[href*='/organisations']")
        cancel_btn.click()

    def enter_site_name(self, site_name):
        self.driver.find_element_by_id("site.name").send_keys(site_name)

    def enter_address_line_1(self, address_line_1):
        self.driver.find_element_by_id("site.address.address_line_1").send_keys(address_line_1)

    def enter_address_line_2(self, address_line_2):
        self.driver.find_element_by_id("site.address.address_line_2").send_keys(address_line_2)

    def enter_zip_code(self, zip_code):
        self.driver.find_element_by_id("site.address.postcode").send_keys(zip_code)

    def enter_city(self, city):
        self.driver.find_element_by_id("site.address.city").send_keys(city)

    def enter_state(self, state):
        self.driver.find_element_by_id("site.address.region").send_keys(state)

    def enter_country(self, country):
        self.driver.find_element_by_id("site.address.country").send_keys(country)
        self.driver.find_element_by_id("site.address.country").send_keys(Keys.RETURN)

    def enter_email(self, email):
        self.driver.find_element_by_id("user.email").send_keys(email)

    def enter_first_name(self, first_name):
        self.driver.find_element_by_id("user.first_name").send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element_by_id("user.last_name").send_keys(last_name)

    def enter_password(self, password):
        self.driver.find_element_by_id("user.password").send_keys(password)

    def click_manage_organisations_link(self):
        self.driver.find_element_by_id("lite-user-menu-button").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("a[href*='/organisations/']").click()

    def click_new_organisation(self):
        self.driver.find_element_by_css_selector("a[href*='/register']").click()

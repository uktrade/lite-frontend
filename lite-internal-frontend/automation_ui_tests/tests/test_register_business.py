import os
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import logging
from automation_ui_tests.pages.department_of_international_trade_hub_page import DepartmentOfInternationalTradeHub
from .cfg.test_configuration import TestConfiguration
config = TestConfiguration


class RegisterBusinessTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        project_root = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(project_root)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.implicitly_wait(10)

        cls.driver.get(config.get_url())

    def test_register_a_business(self):
        driver = self.driver

        dit_hub_page = DepartmentOfInternationalTradeHub(driver)

        manage_organisations_btn = driver.find_element_by_css_selector("a[href*='/organisations']")
        manage_organisations_btn.click()

        # New Organisation
        logging.info("Registering a new business")
        new_organisation_btn = driver.find_element_by_css_selector("a[href*='/register']")
        new_organisation_btn.click()

        logging.info("Entering details")
        business_name_input = driver.find_element_by_id("name")

        eori_number_input = driver.find_element_by_id("eori_number")
        sic_number_input = driver.find_element_by_id("sic_number")
        vat_number_input = driver.find_element_by_id("vat_number")
        company_registration_number = driver.find_element_by_id("registration_number")
        address_input = driver.find_element_by_id("address")
        admin_user_email_input = driver.find_element_by_id("admin_user_email")

        nowId = str(datetime.datetime.now())
        business_name_input.send_keys("Test Business " + nowId)
        eori_number_input.send_keys("GB987654312000")
        sic_number_input.send_keys("73200")
        vat_number_input.send_keys("123456789")
        company_registration_number.send_keys("000000011")
        address_input.send_keys("123 Cobalt Street")
        admin_user_email_input.send_keys("joe@bloss.com")

        logging.info("Submitting...")
        submit = driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

        registration_complete_message = driver.find_element_by_tag_name("h1").text
        assert "Registration complete" == registration_complete_message
        logging.info("Application Submitted")

        dit_hub_page.go_to()

        # verify application is in organisations list
        show_registered_organisations = driver.find_element_by_css_selector("a[href*='/organisations']")
        show_registered_organisations.click()

        self.assertTrue(self.is_element_present(By.XPATH,"//*[text()[contains(.,'"+ nowId +"')]]"))

    def test_cancel_register_a_business(self):
        driver = self.driver
        manage_organisations_btn = driver.find_element_by_css_selector("a[href*='/organisations']")
        manage_organisations_btn.click()

        # New Organisation
        logging.info("Registering a new business")
        new_organisation_btn = driver.find_element_by_css_selector("a[href*='/register']")
        new_organisation_btn.click()

        logging.info("Cancelling...")
        cancel_btn = driver.find_element_by_css_selector("a[href*='/organisations']")
        cancel_btn.click()

        title = driver.title
        assert "Organisations" in title

        logging.info("Application Cancelled")

    def test_cannot_submit_without_required_fields(self):
        driver = self.driver
        manage_organisations_btn = driver.find_element_by_css_selector("a[href*='/organisations']")
        manage_organisations_btn.click()

        # New Organisation
        logging.info("Registering a new business")
        new_organisation_btn = driver.find_element_by_css_selector("a[href*='/register']")
        new_organisation_btn.click()

        logging.info("clicked submit")
        submit = driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

        driver.find_element_by_id("error-summary-title").is_displayed()

        title = driver.title
        assert "Overview" not in title

        logging.info("Test Complete")

    @classmethod
    def tearDown(inst):
        # close the browser window
        inst.driver.quit()

    def is_element_present(self, how, what):
        """
        Helper method to confirm the presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

if __name__ == '__main__':
    unittest.main(verbosity=2)
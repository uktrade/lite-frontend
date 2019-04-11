import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from automation_ui_tests.pages.department_of_international_trade_hub_page import DepartmentOfInternationalTradeHub
from automation_ui_tests.pages.exporter_hub import ExporterHub
import logging
import datetime
from .cfg.test_configuration import TestConfiguration
config = TestConfiguration


class ManageCasesTest(unittest.TestCase):
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

    def test_view_submitted_cases_in_work_queue(self):
        driver = self.driver
        exporterHub = ExporterHub(driver)
        dit_hub_page = DepartmentOfInternationalTradeHub(driver)

        logging.info("Test Started")

        # Submit application
        logging.info("submitting application on Exporter Hub")
        exporterHub.go_to()
        self.driver.find_element_by_css_selector("a[href*='/new-application/']").click()
        self.driver.find_element_by_css_selector("a[href*='/start']").click()
        appTimeId = str(datetime.datetime.now())
        self.driver.find_element_by_id("name").send_keys("Test App" + appTimeId)
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("control_code").send_keys("code123")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("destination").send_keys("Cuba")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("usage").send_keys("shooting usage")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("activity").send_keys("Proliferation")
        exporterHub.click_save_and_continue()
        appId = self.driver.current_url[-36:]
        self.driver.find_element_by_css_selector("button[type*='submit']").click()
        logging.info("Application submitted")

        # navigate to DIT Hub page
        dit_hub_page.go_to()
        logging.info("Navigated to Department Of International Trade Hub")

        # dit_hub_page.click_manage_cases_btn()
        # logging.info("Clicked onto Manage Cases")

        # Verify Case is in the New Cases Work Queue
        logging.info("Verifying Case is in the New Cases Work Queue")
        cases_table = self.driver.find_element_by_class_name("lite-table")
        self.assertTrue(self.is_element_present(By.XPATH,"//*[text()[contains(.,'" + appId + "')]]"))
        logging.info("Application found in work queue")

        # check details page
        logging.info("Verifying the details of a specific case in a work queue...")

        driver.find_element_by_xpath("//*[text()[contains(.,'" + appId + "')]]").click()

        details = driver.find_elements_by_css_selector(".lite-heading-s")
        try:
            for header in details:
                if header.text == "CREATED BY":
                    created_by_detail = header.find_element_by_xpath("./following-sibling::p").text
                    assert created_by_detail == "John Smith"
                    logging.info("created by: " + created_by_detail)
                if header.text == "ACTIVITY":
                    activity_detail = header.find_element_by_xpath("./following-sibling::p").text
                    assert activity_detail == "Proliferation"
                    logging.info("activity: " + activity_detail)
                # if header.text == "LAST UPDATED":
                #     last_updated_detail = header.find_element_by_xpath("./following-sibling::p").text
                #     assert last_updated_detail == ""
                if header.text == "CONTROL CODE":
                    control_code_detail = header.find_element_by_xpath("./following-sibling::p").text
                    assert control_code_detail == "code123"
                    logging.info("control code: "+ control_code_detail)
                if header.text == "DESTINATION":
                    destination_details = header.find_element_by_xpath("./following-sibling::p").text
                    assert destination_details == "Cuba"
                    logging.info("destination: " + destination_details)
                if header.text == "USAGE":
                    usage_detail = header.find_element_by_xpath("./following-sibling::p").text
                    assert usage_detail == "shooting usage"
                    logging.info("usage: " + usage_detail)
        except NoSuchElementException:
                logging.error("Applications details not found")

        logging.info("Test Complete")

    def test_change_status(self):
        driver = self.driver
        exporterHub = ExporterHub(driver)
        dit_hub_page = DepartmentOfInternationalTradeHub(driver)

        logging.info("Test Started")

        # Submit application
        logging.info("submitting application on Exporter Hub")
        exporterHub.go_to()
        self.driver.find_element_by_css_selector("a[href*='/new-application/']").click()
        self.driver.find_element_by_css_selector("a[href*='/start']").click()
        appTimeId = str(datetime.datetime.now())
        self.driver.find_element_by_id("name").send_keys("Test App" + appTimeId)
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("control_code").send_keys("code123")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("destination").send_keys("Cuba")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("usage").send_keys("shooting usage")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("activity").send_keys("Proliferation")
        exporterHub.click_save_and_continue()
        appId = self.driver.current_url[-36:]
        self.driver.find_element_by_css_selector("button[type*='submit']").click()
        logging.info("Application submitted")

        # navigate to DIT Hub page
        dit_hub_page.go_to()
        logging.info("Navigated to Department Of International Trade Hub")

        # Verify Case is in the New Cases Work Queue
        logging.info("Verifying Case is in the New Cases Work Queue")
        cases_table = self.driver.find_element_by_class_name("lite-table")
        self.assertTrue(self.is_element_present(By.XPATH,"//*[text()[contains(.,'" + appId + "')]]"))
        logging.info("Application found in work queue")

        # check details page
        logging.info("Verifying the details of a specific case in a work queue...")

        driver.find_element_by_xpath("//*[text()[contains(.,'" + appId + "')]]").click()

        # Progress application
        progress_app_btn = driver.find_element_by_xpath("//*[text()[contains(.,'Progress')]]")
        progress_app_btn.click()

        # case_status_dropdown = //select[@id='status']/option[text()='Submitted']

        case_status_dropdown = Select(driver.find_element_by_id('status'))
        # select by visible text
        case_status_dropdown.select_by_visible_text('Under review')

        save_btn = driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]")
        save_btn.click()

        details = driver.find_elements_by_css_selector(".lite-heading-s")
        for header in details:
            if header.text == "STATUS":
                created_by_detail = header.find_element_by_xpath("./following-sibling::p").text
                assert created_by_detail == "Under review"

        dit_hub_page.go_to()

        # Check application status is changed
        status = driver.find_element_by_xpath(
            "//*[text()[contains(.,'" + appId + "')]]/../following-sibling::td[last()]")
        assert status.is_displayed()
        assert status.text == "Under review"

        print("Test Complete")



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
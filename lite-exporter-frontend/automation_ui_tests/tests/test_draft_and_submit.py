from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from automation_ui_tests.pages.exporter_hub_page import ExporterHubPage
from automation_ui_tests.pages.apply_for_a_licence_page import ApplyForALicencePage

class DraftTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.implicitly_wait(10)

        # navigate to the application home page
        cls.driver.get("https://lite-exporter-frontend-uat.london.cloudapps.digital/")


    def test_start_draft_application(self):
        print("Test Started")
        driver = self.driver

        exporter_hub = ExporterHubPage(driver)
        apply_for_licence = ApplyForALicencePage(driver)

        exporter_hub.click_apply_for_a_licence()
        print("Clicked apply for a licence")

        apply_for_licence.click_start_btn()
        print("Clicked start button")

        nowId = str(datetime.datetime.now())
        apply_for_licence.enter_name_or_reference_for_application("TestApp " + nowId)
        apply_for_licence.click_save_and_continue()
        print("Entered name of application and clicked save and continue")

        apply_for_licence.enter_control_code("000T")
        apply_for_licence.click_save_and_continue()
        print("Entered control code and clicked save and continue")

        apply_for_licence.enter_destination("Cuba")
        apply_for_licence.click_save_and_continue()
        print("Entered Destination and clicked save and continue")

        apply_for_licence.enter_usage("communication")
        apply_for_licence.click_save_and_continue()
        print("Entered usage and clicked save and continue")

        apply_for_licence.enter_activity("Proliferation")
        apply_for_licence.click_save_and_continue()
        print("Entered Activity and clicked save and continue")

        assert "Overview" in self.driver.title
        print("On the application overview page")

        appId = self.driver.current_url[-36:]
        self.driver.get("https://lite-exporter-frontend-uat.london.cloudapps.digital/")
        print("On Exporter Hub Page")

        # verify application is in drafts
        exporter_hub.click_drafts()
        print("Clicked drafts")

        drafts_table = self.driver.find_element_by_class_name("lite-table")
        drafts_table.find_element_by_xpath(".//td/a[contains(@href,'" + appId + "')]").click()
        print("application found in list")
        print("clicked to open application")

        assert "Overview" in self.driver.title

        appName = self.driver.find_element_by_tag_name("h2").text
        assert "TestApp" in appName
        print("application opened to application overview")

        apply_for_licence.click_delete_application()

        print("Test Complete")

    def test_submit_application(self):
        print("Test Started")
        driver = self.driver

        exporter_hub = ExporterHubPage(driver)
        apply_for_licence = ApplyForALicencePage(driver)

        exporter_hub.click_apply_for_a_licence()
        print("Clicked apply for a licence")

        apply_for_licence.click_start_btn()
        print("Clicked start button")

        nowId = str(datetime.datetime.now())
        apply_for_licence.enter_name_or_reference_for_application("TestApp "+nowId)
        apply_for_licence.click_save_and_continue()
        print("Entered name of application and clicked save and continue")

        apply_for_licence.enter_control_code("000T")
        apply_for_licence.click_save_and_continue()
        print("Entered control code and clicked save and continue")

        apply_for_licence.enter_destination("Cuba")
        apply_for_licence.click_save_and_continue()
        print("Entered Destination and clicked save and continue")

        apply_for_licence.enter_usage("communication")
        apply_for_licence.click_save_and_continue()
        print("Entered usage and clicked save and continue")

        apply_for_licence.enter_activity("Proliferation")
        apply_for_licence.click_save_and_continue()
        print("Entered Activity and clicked save and continue")

        assert "Overview" in self.driver.title
        print("On the application overview page")

        apply_for_licence.click_submit_application()

        application_complete = self.driver.find_element_by_tag_name("h1").text
        assert "Application complete" in application_complete

        self.driver.get("https://lite-exporter-frontend-uat.london.cloudapps.digital/")
        print("On Exporter Hub Page")

        # verify application is in drafts
        exporter_hub.click_applications()
        print("Clicked Applications")

        self.assertTrue(self.is_element_present(By.XPATH,"//*[text()[contains(.,'" + nowId + "')]]"))
        print("application found in submitted applications list")

        print("Test Complete")


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def is_element_present(self, how, what):
        """
        Helper method to confirm the presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DraftTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
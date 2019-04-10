from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from automation_ui_tests.pages.exporter_hub_page import ExporterHubPage
from automation_ui_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from automation_ui_tests.pages.applications_page import ApplicationsPage


class DraftTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        project_root = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(project_root)
        print("dir:" + base_dir)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.implicitly_wait(10)

        # navigate to the application home page
        exporter_hub = ExporterHubPage(cls)
        cls.driver.get(exporter_hub.url)

    def test_start_draft_application(self):
        print("Test Started")
        driver = self.driver

        exporter_hub = ExporterHubPage(driver)
        apply_for_licence = ApplyForALicencePage(driver)

        exporter_hub.go_to()
        exporter_hub.click_apply_for_a_licence()
        print("Clicked apply for a licence")

        apply_for_licence.click_start_now_btn()
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
        exporter_hub.go_to()
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
        assert 'Exporter Hub - LITE' in driver.title

        print("Test Complete")

    def test_submit_application(self):
        print("Test Started")
        driver = self.driver

        exporter_hub = ExporterHubPage(driver)
        apply_for_licence = ApplyForALicencePage(driver)

        exporter_hub.go_to()
        exporter_hub.click_apply_for_a_licence()
        print("Clicked apply for a licence")

        apply_for_licence.click_start_now_btn()
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

        exporter_hub.go_to()
        print("On Exporter Hub Page")

        # verify application is in drafts
        exporter_hub.click_applications()
        print("Clicked Applications")

        self.assertTrue(self.is_element_present(By.XPATH,"//*[text()[contains(.,'" + nowId + "')]]"))
        print("application found in submitted applications list")

        # Check application status is Submitted
        status = driver.find_element_by_xpath("//*[text()[contains(.,'" + nowId + "')]]/following-sibling::td[last()]")
        assert status.is_displayed()
        assert status.text == "Submitted"
        print("Test Complete")

    def test_must_enter_fields_for_application(self):
        print("Test Started")
        driver = self.driver

        assert 'Exporter Hub - LITE' in driver.title

        exporter_hub = ExporterHubPage(driver)
        apply_for_licence = ApplyForALicencePage(driver)
        exporter_hub.click_apply_for_a_licence()
        print("Clicked apply for a licence")
        apply_for_licence.click_start_now_btn()
        print("Clicked start button")

        print("no name or reference entered")
        print("clicked save and continue")
        apply_for_licence.click_save_and_continue()

        element = driver.find_element_by_css_selector('.govuk-error-summary')
        assert element.is_displayed()
        assert 'Name: This field may not be blank.' in element.text
        print("Error displayed successfully")

        apply_for_licence.enter_name_or_reference_for_application("a")
        apply_for_licence.click_save_and_continue()

        print("no control code entered")
        print("clicked save and continue")
        apply_for_licence.click_save_and_continue()

        element = driver.find_element_by_css_selector('.govuk-error-summary')
        assert element.is_displayed()
        assert 'Control_Code: This field may not be blank.' in element.text
        print("Error displayed successfully")

        apply_for_licence.enter_control_code("b")
        apply_for_licence.click_save_and_continue()

        print("no Destination entered")
        print("clicked save and continue")
        apply_for_licence.click_save_and_continue()

        element = driver.find_element_by_css_selector('.govuk-error-summary')
        assert element.is_displayed()
        assert 'Destination: This field may not be blank.' in element.text
        print("Error displayed successfully")

        apply_for_licence.enter_destination("c")
        apply_for_licence.click_save_and_continue()

        print("no Usage entered")
        print("clicked save and continue")
        apply_for_licence.click_save_and_continue()

        element = driver.find_element_by_css_selector('.govuk-error-summary')
        assert element.is_displayed()
        assert 'Usage: This field may not be blank.' in element.text
        print("Error displayed successfully")

        apply_for_licence.enter_usage("d")
        apply_for_licence.click_save_and_continue()

        print("no Activity entered")
        print("clicked save and continue")
        apply_for_licence.click_save_and_continue()

        element = driver.find_element_by_css_selector('.govuk-error-summary')
        assert element.is_displayed()
        assert 'Activity: This field may not be blank.' in element.text
        print("Error displayed successfully")

        apply_for_licence.enter_activity("e")
        apply_for_licence.click_save_and_continue()
        print("Error displayed successfully")
        print("Test Complete")

        apply_for_licence.click_delete_application()
        assert 'Exporter Hub - LITE' in driver.title

    def test_status_column_and_refresh_btn_on_applications(self):
        print("Test Started")
        driver = self.driver
        exporter_hub = ExporterHubPage(driver)
        applications = ApplicationsPage(driver)

        exporter_hub.click_applications()
        print("navigated to applications page")

        self.assertTrue(driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed())
        print("Status column is displayed")

        applications.click_refresh_btn()
        print("clicked refresh button")

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
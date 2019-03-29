from selenium import webdriver
import unittest
import sys
import os
from ui_automation.pages.exporter_hub_page import ExporterHubPage
from ui_automation.pages.apply_for_a_licence_page import ApplyForALicencePage


class DraftTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # get the path of ChromeDriverServer
        project_root = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(project_root)
        print("dir:" + base_dir)

        chrome_driver_path = base_dir + "/drivers/chromedriver"
        # create a new Chrome session
        cls.driver = webdriver.Chrome(chrome_driver_path)
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

        # navigate to the application home page
        cls.driver.get("https://lite-exporter-frontend-dev.london.cloudapps.digital/")

    def test_start_draft_application(self):
        # check language options on Home page
        driver = self.driver

        exporter_hub = ExporterHubPage(driver)
        apply_for_licence = ApplyForALicencePage(driver)

        exporter_hub.click_apply_for_a_licence()
        apply_for_licence.click_start_btn()

        apply_for_licence.enter_name_or_reference_for_application("TestApp")
        apply_for_licence.click_save_and_continue()

        apply_for_licence.enter_control_code("000T")
        apply_for_licence.click_save_and_continue()

        apply_for_licence.enter_destination("Cuba")
        apply_for_licence.click_save_and_continue()

        apply_for_licence.enter_usage("communication")
        apply_for_licence.click_save_and_continue()

        apply_for_licence.enter_activity("Proliferation")
        apply_for_licence.click_save_and_continue()

        assert "Overview" in self.driver.title

        appId = self.driver.current_url[-36:]
        self.driver.get("https://lite-exporter-frontend-dev.london.cloudapps.digital/")

        #verify application is in drafts
        exporter_hub.click_drafts()

        drafts_table = self.driver.find_element_by_class_name("lite-table")
        drafts_table.find_element_by_xpath(".//td/a[contains(@href,'" + appId + "')]").click()

        assert "Overview" in self.driver.title

        appName = self.driver.find_element_by_tag_name("h2").text
        assert "TestApp" in appName

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

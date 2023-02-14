from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class AddMemberPage(BasePage):
    def enter_email(self, email):
        email_tb = self.driver.find_element(by=By.ID, value="email")
        email_tb.send_keys(email)

    def check_all_sites(self):
        site_checkboxes = self.driver.find_elements_by_name("sites[]")
        for checkbox in site_checkboxes:
            checkbox.click()

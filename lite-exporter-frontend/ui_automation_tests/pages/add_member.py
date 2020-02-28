from ui_automation_tests.shared.BasePage import BasePage


class AddMemberPage(BasePage):
    def enter_email(self, email):
        email_tb = self.driver.find_element_by_id("email")
        email_tb.send_keys(email)

    def check_all_sites(self):
        site_checkboxes = self.driver.find_elements_by_name("sites[]")
        for checkbox in site_checkboxes:
            checkbox.click()

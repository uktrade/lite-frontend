from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class SecurityApprovalPage(BasePage):
    def set_exporting_classified_product(self, choice):
        value = {
            "No": "False",
            "Yes": "True",
        }[choice]

        self.driver.find_element(
            by=By.XPATH,
            value=f"//input[@type='radio' and contains(@name, 'is_mod_security_approved') and @value='{value}']",
        ).click()

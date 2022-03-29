from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class DenialRecordsPage(BasePage):
    def get_row_for_name(self, name):
        return self.driver.find_element(
            by=By.XPATH, value=f"//table[@id='table-denials']/tbody/tr[td[contains(text(), '{name}')]][1]"
        )

    def select_row_for_name(self, name):
        self.get_row_for_name(name).find_element(by=By.XPATH, value="//input[@type='checkbox']").click()

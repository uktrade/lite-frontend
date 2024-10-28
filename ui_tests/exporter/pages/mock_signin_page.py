from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class MockSigninPage(BasePage):
    def enter_email(self, email):
        email_input = self.driver.find_element(By.NAME, value="email")
        email_input.clear()
        email_input.send_keys(email)

    def click_submit(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value="[type='submit']").click()

    def sign_in(self, email):
        self.enter_email(email)
        self.click_submit()

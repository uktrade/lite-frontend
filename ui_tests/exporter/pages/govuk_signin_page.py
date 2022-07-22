from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from ui_tests.exporter.pages.BasePage import BasePage


class GovukSigninPage(BasePage):
    LOGIN_SECTION_ID = "login-form"
    EMAIL_INPUT_ID = "email"
    PASSWORD_INPUT_ID = "password"  # noqa
    CREATE_GOVUK_ACCOUNT = "create-account-link"
    SUBMIT_BUTTON_CSS_SELECTOR = "button[type='submit']"
    CONTINUE_BUTTON = ".govuk-button"

    def enter_email(self, email):
        email_input = self.driver.find_element_by_id(self.EMAIL_INPUT_ID)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.driver.find_element_by_id(self.PASSWORD_INPUT_ID)
        password_input.clear()
        password_input.send_keys(password)

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BUTTON_CSS_SELECTOR).click()
    
    def enter_basic_auth(self):
        url = self.driver.current_url
        url = url.replace('https://', 'https://integration-user:winter2021@')
        self.driver.get(url)

    def click_create_govuk_account(self):
        self.driver.find_element_by_id(self.CREATE_GOVUK_ACCOUNT).click()

    def sign_in(self, email, password):
        self.enter_basic_auth()
        self.click_create_govuk_account()
        self.enter_email(email)
        self.click_continue()
        self.enter_password(password)
        self.click_continue()

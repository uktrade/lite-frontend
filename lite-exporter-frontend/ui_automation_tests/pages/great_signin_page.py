from selenium.common.exceptions import NoSuchElementException

from ui_automation_tests.shared.BasePage import BasePage
from ui_automation_tests.shared.tools.utils import set_timeout_to


class GreatSigninPage(BasePage):
    LOGIN_SECTION_ID = "login-form"
    EMAIL_INPUT_ID = "id_login"
    PASSWORD_INPUT_ID = "id_password"  # noqa
    SUBMIT_BUTTON_CSS_SELECTOR = "button[type='submit']"
    ACCEPT_COOKIES_TEXT = "Accept all cookies"

    def enter_email(self, form, email):
        email_input = form.find_element_by_id(self.EMAIL_INPUT_ID)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, form, password):
        password_input = form.find_element_by_id(self.PASSWORD_INPUT_ID)
        password_input.clear()
        password_input.send_keys(password)

    def click_sign_in(self, form):
        form.find_element_by_css_selector(self.SUBMIT_BUTTON_CSS_SELECTOR).click()

    def handle_accept_cookies_popup(self):
        try:
            set_timeout_to(self.driver, 0)
            self.driver.find_element_by_link_text(self.ACCEPT_COOKIES_TEXT).click()
            set_timeout_to(self.driver, 10)
        except NoSuchElementException:
            pass

    def sign_in(self, email, password):
        self.handle_accept_cookies_popup()
        form = self.driver.find_element_by_id(self.LOGIN_SECTION_ID)
        self.enter_email(form, email)
        self.enter_password(form, password)
        self.click_sign_in(form)

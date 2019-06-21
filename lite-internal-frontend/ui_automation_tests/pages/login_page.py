class LoginPage():

    def __init__(self, driver):
        self.driver = driver
        self.login_field = driver.find_element_by_name("username")
        self.password_field = driver.find_element_by_name("password")
        self.external_gov_login_message = ".container p"
        self.submit_button = driver.find_element_by_css_selector("[type='submit']")

    def type_into_login_field(self, text):
        self.login_field.send_keys(text)

    def type_into_password_field(self, text):
        self.password_field.send_keys(text)

    def click_on_submit_button(self):
        self.submit_button.click()

    def get_text_of_gov_login_message(self):
        return self.driver.find_element_by_css_selector(self.external_gov_login_message).text

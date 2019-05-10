class ExporterHub():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

    def go_to(self, url):
        self.driver.get(url)

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[action*='submit']").click()

    def click_submit_application(self):
        self.driver.find_element_by_css_selector("button[type*='submit']").click()

    def click_applications_btn(self):
        self.driver.find_element_by_css_selector("a[href*='/applications/']").click()

    def enter_email(self, email):
        email_tb = self.driver.find_element_by_id("email")
        email_tb.clear()
        email_tb.send_keys(email)

    def enter_password(self, password):
        password_tb = self.driver.find_element_by_id("password")
        password_tb.send_keys(password)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()

    def click_submit(self):
        self.driver.find_element_by_css_selector(".govuk-button").click()

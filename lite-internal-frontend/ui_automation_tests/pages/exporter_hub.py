class ExporterHub():

    # called every time you create an object for this class
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


    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector("a[href*='/new-application/']").click()

    def click_start(self):
        self.driver.find_element_by_css_selector("a[href*='/start']").click()

    def enter_name_for_application(self, name):
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys(name)

    def enter_destination(self, destination):
        self.driver.find_element_by_id("destination").clear()
        self.driver.find_element_by_id("destination").send_keys(destination)

    def enter_usage(self, usage):
        self.driver.find_element_by_id("usage").clear()
        self.driver.find_element_by_id("usage").send_keys(usage)

    def enter_activity(self, activity):
        self.driver.find_element_by_id("activity").clear()
        self.driver.find_element_by_id("activity").send_keys(activity)

    def create_application(self, name, destination, usage, activity):
        self.click_apply_for_a_licence()
        self.click_start()
        self.enter_name_for_application(name)
        self.click_save_and_continue()
        self.enter_destination(destination)
        self.click_save_and_continue()
        self.enter_usage(usage)
        self.click_save_and_continue()
        self.enter_activity(activity)
        self.click_submit()
        self.click_submit_application()


    def click_sites(self):
        self.driver.find_element_by_css_selector("a[href='/sites/']").click()

    def click_new_site(self):
        self.driver.find_element_by_css_selector("a[href*='/sites/new/']").click()

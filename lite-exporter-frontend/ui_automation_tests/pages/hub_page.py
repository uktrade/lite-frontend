class Hub():

    def __init__(self, driver):
        self.driver = driver
        self.drafts_btn = "a[href*='/drafts/']"  # CSS
        self.sites_btn = "[href*='/sites/']"  # CSS
        self.application_btn = "a[href*='/applications/']"  # CSS
        self.add_user_button = "a[href*='/users/add']"  # CSS
        self.users_button = "a[href='/users/']"  # CSS
        self.first_name_field = "first_name"  # ID
        self.last_name_field = "last_name"  # ID
        self.last_name_field = "last_name"  # ID
        self.email_field = "email"  # ID
        self.password_field = "password"  # ID
        self.applications_tile = '.lite-tiles [href="/applications/"] p'  # ID

    def click_drafts(self):
        self.driver.find_element_by_css_selector(self.drafts_btn).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.application_btn).click()

    def click_add_user_button(self):
        self.driver.find_element_by_css_selector(self.add_user_button).click()

    def click_on_users_button(self):
        self.driver.find_element_by_css_selector(self.users_button).click()

    def enter_first_name(self, first_name):
        self.driver.find_element_by_id(self.first_name_field).clear()
        self.driver.find_element_by_id(self.first_name_field).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element_by_id(self.last_name_field).clear()
        self.driver.find_element_by_id(self.last_name_field).send_keys(last_name)

    def enter_email(self, email):
        self.driver.find_element_by_id(self.email_field).clear()
        self.driver.find_element_by_id(self.email_field).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element_by_id(self.password_field).clear()
        self.driver.find_element_by_id(self.password_field).send_keys(password)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_btn).click()

    def get_text_of_application_tile(self):
        return self.driver.find_element_by_css_selector(self.applications_tile).text

    def return_number_of_notifications(self):
        text_of_new_notifications = self.driver.find_element_by_css_selector(
            self.applications_tile).text
        total_of_notifications = int((text_of_new_notifications.split('have '))[1].split(' new')[0])
        return total_of_notifications


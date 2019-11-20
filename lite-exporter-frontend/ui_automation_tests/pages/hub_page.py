from shared.BasePage import BasePage


class Hub(BasePage):

    SWITCH_LINK = "switch-link"  # ID
    DRAFTS_BTN = "a[href*='/drafts/']"  # CSS
    SITES_BTN = "[href*='/sites/']"  # CSS
    APPLICATION_BTN = "a[href*='/applications/']"  # CSS
    ADD_USER_BUTTON = "a[href*='/users/add']"  # CSS
    USERS_BUTTON = "a[href='/users/']"  # CSS
    FIRST_NAME_FIELD = "first_name"  # ID
    LAST_NAME_FIELD = "last_name"  # ID
    EMAIL_FIELD = "email"  # ID
    PASSWORD_FIELD = "password"  # ID  # noqa
    APPLICATIONS_TILE = '.app-tiles [href="/applications/"] p'  # ID

    def click_drafts(self):
        self.driver.find_element_by_css_selector(self.DRAFTS_BTN).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.APPLICATION_BTN).click()

    def click_add_user_button(self):
        self.driver.find_element_by_css_selector(self.ADD_USER_BUTTON).click()

    def click_on_users_button(self):
        self.driver.find_element_by_css_selector(self.USERS_BUTTON).click()

    def enter_first_name(self, first_name):
        self.driver.find_element_by_id(self.FIRST_NAME_FIELD).clear()
        self.driver.find_element_by_id(self.FIRST_NAME_FIELD).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element_by_id(self.LAST_NAME_FIELD).clear()
        self.driver.find_element_by_id(self.LAST_NAME_FIELD).send_keys(last_name)

    def enter_email(self, email):
        self.driver.find_element_by_id(self.EMAIL_FIELD).clear()
        self.driver.find_element_by_id(self.EMAIL_FIELD).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element_by_id(self.PASSWORD_FIELD).clear()
        self.driver.find_element_by_id(self.PASSWORD_FIELD).send_keys(password)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.SITES_BTN).click()

    def click_switch_link(self):
        self.driver.find_element_by_id(self.SWITCH_LINK).click()

    def get_text_of_application_tile(self):
        return self.driver.find_element_by_css_selector(self.APPLICATIONS_TILE).text

    def return_number_of_notifications(self):
        text_of_new_notifications = self.driver.find_element_by_css_selector(self.APPLICATIONS_TILE).text
        if "You have" in text_of_new_notifications:
            total_of_notifications = int((text_of_new_notifications.split("have "))[1].split(" new")[0])
        else:
            total_of_notifications = 0
        return total_of_notifications

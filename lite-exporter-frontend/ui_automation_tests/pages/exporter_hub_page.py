import time

from shared.BasePage import BasePage


class ExporterHubPage(BasePage):

    APPLY_FOR_A_LICENCE_BTN = "a[href*='/apply-for-a-licence/']"
    APPLICATIONS_BTN = "a[href*='/applications/']"
    MY_GOODS_BTN = "a[href*='/goods/']"
    ADD_A_GOOD_BTN = "a[href*='/goods/add/']"
    USERS_BTN = "a[href='/users/']"
    SITES_BTN = "a[href='/sites/']"
    SITES_LINK = "a[href*='sites']"
    END_USER_ADVISORY_TILE = "a[href*='/end-users/']"
    RAISE_HMRC_QUERY_BTN = "a[href*='/raise-a-query/"

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.APPLY_FOR_A_LICENCE_BTN).click()

    def click_raise_hmrc_query(self):
        self.driver.find_element_by_css_selector(self.RAISE_HMRC_QUERY_BTN).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.APPLICATIONS_BTN).click()

    def click_end_user_advisories(self):
        self.driver.find_element_by_css_selector(self.END_USER_ADVISORY_TILE).click()

    def enter_email(self, email):
        email_tb = self.driver.find_element_by_name("login")
        email_tb.clear()
        email_tb.send_keys(email)

    def enter_password(self, password):
        password_tb = self.driver.find_element_by_name("password")
        password_tb.send_keys(password)

    def login(self, email, password):
        if "logout" in self.driver.current_url:
            self.driver.find_element_by_xpath("//a[text()[contains(.,'Log In')]]").click()

        if self.driver.find_element_by_link_text("Accept all cookies"):
            self.driver.find_element_by_link_text("Accept all cookies").click()

        time.sleep(1)
        self.enter_email(email)
        self.enter_password(password)
        self.driver.find_element_by_xpath("//button[text()[contains(.,'Sign in')]]").click()
        time.sleep(1)

    def click_my_goods(self):
        self.driver.find_element_by_css_selector(self.MY_GOODS_BTN).click()

    def click_users(self):
        self.driver.find_element_by_css_selector(self.USERS_BTN).click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector("a[href*='/users/profile/']").click()

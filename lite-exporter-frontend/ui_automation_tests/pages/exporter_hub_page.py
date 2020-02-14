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
    USER_PROFILE_BTN = "a[href*='/users/profile/']"

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.APPLY_FOR_A_LICENCE_BTN).click()

    def click_raise_hmrc_query(self):
        self.driver.find_element_by_css_selector(self.RAISE_HMRC_QUERY_BTN).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.APPLICATIONS_BTN).click()

    def click_end_user_advisories(self):
        self.driver.find_element_by_css_selector(self.END_USER_ADVISORY_TILE).click()

    def click_my_goods(self):
        self.driver.find_element_by_css_selector(self.MY_GOODS_BTN).click()

    def click_users(self):
        self.driver.find_element_by_css_selector(self.USERS_BTN).click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.USER_PROFILE_BTN).click()

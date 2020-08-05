from ui_automation_tests.pages.BasePage import BasePage


class ExporterHubPage(BasePage):
    BUTTON_APPLY_FOR_A_LICENCE_ID = "link-apply"
    BUTTON_APPLICATIONS_ID = "link-applications"
    BUTTON_PRODUCTS_ID = "link-products"
    BUTTON_PROFILE_ID = "link-profile"
    BUTTON_EUA_ID = "link-eua"
    BUTTON_LICENCES_ID = "link-licences"
    BUTTON_HMRC_QUERY_ID = "link-hmrc-query"
    BUTTON_OPEN_LICENCE_RETURNS_ID = "link-open-licence-returns"
    BUTTON_COMPLIANCE_ID = "link-compliance"
    USER_PROFILE_BTN = "a[href*='/users/profile/']"

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_id(self.BUTTON_APPLY_FOR_A_LICENCE_ID).click()

    def click_raise_hmrc_query(self):
        self.driver.find_element_by_id(self.BUTTON_HMRC_QUERY_ID).click()

    def click_applications(self):
        self.driver.find_element_by_id(self.BUTTON_APPLICATIONS_ID).click()

    def click_end_user_advisories(self):
        self.driver.find_element_by_id(self.BUTTON_EUA_ID).click()

    def click_my_goods(self):
        self.driver.find_element_by_id(self.BUTTON_PRODUCTS_ID).click()

    def click_licences(self):
        self.driver.find_element_by_id(self.BUTTON_LICENCES_ID).click()

    def click_manage_my_organisation_tile(self):
        self.driver.find_element_by_id(self.BUTTON_PROFILE_ID).click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.USER_PROFILE_BTN).click()

    def click_open_licence_returns(self):
        self.driver.find_element_by_id(self.BUTTON_OPEN_LICENCE_RETURNS_ID).click()

    def click_compliance(self):
        self.driver.find_element_by_id(self.BUTTON_COMPLIANCE_ID).click()

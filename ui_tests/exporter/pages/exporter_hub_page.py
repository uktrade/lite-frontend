from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_by_id


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
        scroll_to_element_by_id(self.driver, self.BUTTON_APPLY_FOR_A_LICENCE_ID)
        self.driver.find_element(by=By.ID, value=self.BUTTON_APPLY_FOR_A_LICENCE_ID).click()

    def click_raise_hmrc_query(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_HMRC_QUERY_ID)
        self.driver.find_element_by_id(self.BUTTON_HMRC_QUERY_ID).click()

    def click_applications(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_APPLICATIONS_ID)
        self.driver.find_element_by_id(self.BUTTON_APPLICATIONS_ID).click()

    def click_end_user_advisories(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_EUA_ID)
        self.driver.find_element_by_id(self.BUTTON_EUA_ID).click()

    def click_my_goods(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_PRODUCTS_ID)
        self.driver.find_element_by_id(self.BUTTON_PRODUCTS_ID).click()

    def click_licences(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_LICENCES_ID)
        self.driver.find_element_by_id(self.BUTTON_LICENCES_ID).click()

    def click_manage_my_organisation_tile(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_PROFILE_ID)
        self.driver.find_element_by_id(self.BUTTON_PROFILE_ID).click()

    def click_user_profile(self):
        scroll_to_element_by_id(self.driver, self.USER_PROFILE_BTN)
        self.driver.find_element_by_css_selector(self.USER_PROFILE_BTN).click()

    def click_open_licence_returns(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_OPEN_LICENCE_RETURNS_ID)
        self.driver.find_element_by_id(self.BUTTON_OPEN_LICENCE_RETURNS_ID).click()

    def click_compliance(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_COMPLIANCE_ID)
        self.driver.find_element_by_id(self.BUTTON_COMPLIANCE_ID).click()

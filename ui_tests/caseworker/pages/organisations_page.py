from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage


class OrganisationsPage(BasePage):

    BUTTON_REGISTER_ORGANISATION_ID = "button-register-organisation"
    BUTTON_REGISTER_HMRC_ORGANISATION_ID = "button-register-hmrc-organisation"
    INPUT_SEARCH_TERM_ID = "search_term"
    IN_REVIEW_TAB_ID = "in_review"
    ACTIVE_TAB_ID = "active"
    AUDIT_TRAIL_ID = "audit-trail"

    def click_new_organisation_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_REGISTER_ORGANISATION_ID).click()

    def click_new_hmrc_organisation_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_REGISTER_HMRC_ORGANISATION_ID).click()

    def search_for_org_in_filter(self, org_name):
        functions.try_open_filters(self.driver)
        self.driver.find_element(by=By.ID, value=self.INPUT_SEARCH_TERM_ID).send_keys(org_name)
        functions.click_apply_filters(self.driver)

    def click_organisation(self, name):
        self.driver.find_element(by=By.LINK_TEXT, value=name).click()

    def go_to_in_review_tab(self):
        self.driver.find_element(by=By.ID, value=self.IN_REVIEW_TAB_ID).click()

    def go_to_active_tab(self):
        self.driver.find_element(by=By.ID, value=self.ACTIVE_TAB_ID).click()

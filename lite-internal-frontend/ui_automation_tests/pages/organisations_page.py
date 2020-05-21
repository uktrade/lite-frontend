from shared import functions
from shared.BasePage import BasePage


class OrganisationsPage(BasePage):

    BUTTON_REGISTER_ORGANISATION_ID = "button-register-organisation"
    BUTTON_REGISTER_HMRC_ORGANISATION_ID = "button-register-hmrc-organisation"
    INPUT_SEARCH_TERM_ID = "search_term"
    IN_REVIEW_TAB_ID = "in_review"
    ACTIVE_TAB_ID = "active"
    AUDIT_TRAIL_ID = "audit-trail"

    def click_new_organisation_button(self):
        self.driver.find_element_by_id(self.BUTTON_REGISTER_ORGANISATION_ID).click()

    def click_new_hmrc_organisation_button(self):
        self.driver.find_element_by_id(self.BUTTON_REGISTER_HMRC_ORGANISATION_ID).click()

    def search_for_org_in_filter(self, org_name):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_SEARCH_TERM_ID).send_keys(org_name)
        self.driver.find_element_by_id("button-apply-filters").click()

    def click_organisation(self, name):
        self.driver.find_element_by_link_text(name).click()

    def go_to_in_review_tab(self):
        self.driver.find_element_by_id(self.IN_REVIEW_TAB_ID).click()

    def go_to_active_tab(self):
        self.driver.find_element_by_id(self.ACTIVE_TAB_ID).click()

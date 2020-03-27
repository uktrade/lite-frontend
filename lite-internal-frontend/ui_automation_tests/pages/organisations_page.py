from shared.BasePage import BasePage


class OrganisationsPage(BasePage):

    BUTTON_REGISTER_ORGANISATION_ID = "button-register-organisation"
    BUTTON_REGISTER_HMRC_ORGANISATION_ID = "button-register-hmrc-organisation"
    INPUT_SEARCH_TERM_ID = "search_term"

    def click_new_organisation_button(self):
        self.driver.find_element_by_id(self.BUTTON_REGISTER_ORGANISATION_ID).click()

    def click_new_hmrc_organisation_button(self):
        self.driver.find_element_by_id(self.BUTTON_REGISTER_HMRC_ORGANISATION_ID).click()

    def search_for_org_in_filter(self, org_name):
        self.driver.find_element_by_id("show-filters-link").click()
        self.driver.find_element_by_id(self.INPUT_SEARCH_TERM_ID).send_keys(org_name)
        self.driver.find_element_by_id("button-apply-filters").click()

    def click_organisation(self, name):
        self.driver.find_element_by_link_text(name).click()

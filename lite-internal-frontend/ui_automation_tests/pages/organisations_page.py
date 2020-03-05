from shared.BasePage import BasePage


class OrganisationsPage(BasePage):

    INPUT_SEARCH_TERM_ID = "search_term"

    def click_new_organisation_btn(self):
        new_organisation_btn = self.driver.find_element_by_css_selector("a[href*='organisations/register']")
        new_organisation_btn.click()

    def search_for_org_in_filter(self, org_name):
        self.driver.find_element_by_id("show-filters-link").click()
        self.driver.find_element_by_id(self.INPUT_SEARCH_TERM_ID).send_keys(org_name)
        self.driver.find_element_by_id("button-apply-filters").click()

from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage


class OrganisationPage(BasePage):

    LINK_ORGANISATION_FLAGS_ID = "link-organisation-flags"
    LINK_EDIT_ORGANISATION_ID = "link-edit-organisation"
    REVIEW_ORGANISATION_BUTTON_ID = "review"
    ORGANISATION_SUMMARY_CSS_SELECTOR = ".govuk-summary-list"
    REVIEW_PARTIAL_ID = "status-"
    ORGANISATION_STATUS_ID = "status"
    WARNING_BANNER_ID = "org_warning"

    def click_edit_organisation_flags(self):
        self.driver.find_element_by_id(self.LINK_ORGANISATION_FLAGS_ID).click()

    def click_edit_organisation_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_ORGANISATION_ID).click()

    def get_organisation_row(self, organisation_id=None):
        if organisation_id:
            row = self.driver.find_element_by_id(organisation_id)
        else:
            row = self.driver.find_element_by_css_selector(".govuk-table__body .govuk-table__row")

        return {
            "name": row.find_element_by_id("name").text,
            "type": row.find_element_by_id("type").text,
            "eori-number": row.find_element_by_id("eori-number").text,
            "sic-number": row.find_element_by_id("sic-number").text,
            "vat-number": row.find_element_by_id("vat-number").text,
        }

    def click_review_organisation(self):
        self.driver.find_element(by=By.ID, value=self.REVIEW_ORGANISATION_BUTTON_ID).click()

    def get_organisation_summary(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.ORGANISATION_SUMMARY_CSS_SELECTOR).text

    def select_approve_organisation(self):
        self.driver.find_element(by=By.ID, value=self.REVIEW_PARTIAL_ID + "active").click()

    def select_reject_organisation(self):
        self.driver.find_element(by=By.ID, value=self.REVIEW_PARTIAL_ID + "rejected").click()

    def get_status(self):
        return self.driver.find_element(by=By.ID, value=self.ORGANISATION_STATUS_ID).text

    def get_warning(self):
        return self.driver.find_element(by=By.ID, value=self.WARNING_BANNER_ID).text

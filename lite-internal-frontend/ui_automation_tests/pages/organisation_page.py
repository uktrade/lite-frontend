from shared.BasePage import BasePage

from ui_automation_tests.shared.tools.helpers import paginated_item_exists


class OrganisationPage(BasePage):

    LINK_ORGANISATION_FLAGS_ID = "link-organisation-flags"
    FLAGS_AREA_SELECTOR = ".app-flag"
    LINK_EDIT_ORGANISATION_ID = "link-edit-organisation"

    def click_edit_organisation_flags(self):
        self.driver.find_element_by_id(self.LINK_ORGANISATION_FLAGS_ID).click()

    def is_organisation_flag_applied(self, flag_name):
        elements = self.driver.find_elements_by_css_selector(self.FLAGS_AREA_SELECTOR)

        for element in elements:
            if flag_name.lower() == element.text.lower():
                return True
        return False

    def click_edit_organisation_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_ORGANISATION_ID).click()

    def get_organisation_row(self, organisation_id=None):
        if organisation_id:
            paginated_item_exists(organisation_id, self.driver)
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

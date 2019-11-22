from shared.BasePage import BasePage


class OrganisationPage(BasePage):

    LINK_ORGANISATION_FLAGS_ID = "link-organisation-flags"
    FLAGS_AREA_SELECTOR = ".app-flag"

    def click_edit_organisation_flags(self):
        self.driver.find_element_by_id(self.LINK_ORGANISATION_FLAGS_ID).click()

    def is_organisation_flag_applied(self, flag_name):
        elements = self.driver.find_elements_by_css_selector(self.FLAGS_AREA_SELECTOR)

        for element in elements:
            if flag_name.lower() == element.text.lower():
                return True
        return False

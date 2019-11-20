from helpers.BasePage import BasePage


class OrganisationPage(BasePage):
    EDIT_ORGANISATION_FLAGS = 'a[href*="/assign-flags/"]'
    FLAGS_AREA = ".app-flag"

    def click_edit_organisation_flags(self):
        edit_flags_btn = self.driver.find_element_by_css_selector(self.EDIT_ORGANISATION_FLAGS)
        edit_flags_btn.click()

    def is_organisation_flag_applied(self, flag_name):
        elements = self.driver.find_elements_by_css_selector(self.FLAGS_AREA)
        for element in elements:
            if flag_name in element.text:
                return True
        return False

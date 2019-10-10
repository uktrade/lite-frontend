class OrganisationPage:
    def __init__(self, driver):
        self.driver = driver
        self.edit_organisation_flags = 'a[href*="/assign-flags/"]'
        self.flags_area = '.app-flag'

    def click_edit_organisation_flags(self):
        edit_flags_btn = self.driver.find_element_by_css_selector(self.edit_organisation_flags)
        edit_flags_btn.click()

    def is_organisation_flag_applied(self, flag_name):
        elements = self.driver.find_elements_by_css_selector(self.flags_area)
        for element in elements:
            if flag_name in element.text:
                return True
        return False

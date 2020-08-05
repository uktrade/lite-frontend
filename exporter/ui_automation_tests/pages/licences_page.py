from ui_automation_tests.pages.BasePage import BasePage


class LicencesPage(BasePage):
    LICENCE_ROW_PARTIAL_ID = "licence-"
    VIEW_LICENCE_PARTIAL_ID = "view-"
    EXPAND_LICENCE_ROW_PARTIAL_ID = "expand-"
    CLEARANCES_TAB_ID = "tab-clearances"
    NLR_TAB_ID = "tab-no_licence_required"

    def licence_row_properties(self, id):
        self.driver.find_element_by_id(self.EXPAND_LICENCE_ROW_PARTIAL_ID + id).click()
        return self.driver.find_element_by_id(self.LICENCE_ROW_PARTIAL_ID + id).text

    def click_clearances_tab(self):
        self.driver.find_element_by_id(self.CLEARANCES_TAB_ID).click()

    def click_nlr_tab(self):
        self.driver.find_element_by_id(self.NLR_TAB_ID).click()

    def click_licence(self, id):
        self.driver.find_element_by_id(self.VIEW_LICENCE_PARTIAL_ID + id).click()

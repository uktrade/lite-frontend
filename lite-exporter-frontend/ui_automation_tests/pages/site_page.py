from ui_automation_tests.shared.BasePage import BasePage


class SitePage(BasePage):
    LINK_CHANGE_NAME_ID = "link-change-name"

    def click_change_name_link(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_NAME_ID).click()

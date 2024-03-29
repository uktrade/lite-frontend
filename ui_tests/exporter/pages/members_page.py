from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.tools.helpers import find_paginated_item_by_id


class MembersPage(BasePage):
    LINK_VIEW_ID_PREFIX = "link-view-"
    BUTTON_ADD_A_MEMBER_ID = "button-add-a-member"
    STATUS_ID = "status"

    def click_view_member_link(self, email: str):
        find_paginated_item_by_id(self.LINK_VIEW_ID_PREFIX + email, self.driver)
        self.driver.find_element(by=By.ID, value=self.LINK_VIEW_ID_PREFIX + email).click()

    def click_add_a_member_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_ADD_A_MEMBER_ID).click()

    def select_filter_status_from_dropdown(self, status):
        select = Select(self.driver.find_element(by=By.ID, value=self.STATUS_ID))
        select.select_by_visible_text(status)

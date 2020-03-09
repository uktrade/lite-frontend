from ui_automation_tests.shared.BasePage import BasePage

from ui_automation_tests.shared.tools.helpers import select_visible_text_from_dropdown, find_paginated_item_by_id


class MembersPage(BasePage):

    LINK_VIEW_ID_PREFIX = "link-view-"
    BUTTON_ADD_A_MEMBER_ID = "button-add-a-member"
    BUTTON_APPLY_FILTER_ID = "button-apply-filters"
    FILTERS_LINK_ID = "show-filters-link"
    STATUS_ID = "status"

    def click_view_member_link(self, email: str):
        find_paginated_item_by_id(self.LINK_VIEW_ID_PREFIX + email, self.driver)
        self.driver.find_element_by_id(self.LINK_VIEW_ID_PREFIX + email).click()

    def click_add_a_member_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_MEMBER_ID).click()

    def click_show_filters_link(self):
        self.driver.find_element_by_id(self.FILTERS_LINK_ID).click()

    def select_filter_status_from_dropdown(self, status):
        select_visible_text_from_dropdown(self.driver.find_element_by_id(self.STATUS_ID), status)

    def click_apply_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTER_ID).click()

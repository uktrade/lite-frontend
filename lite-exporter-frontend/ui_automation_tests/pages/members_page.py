from shared.BasePage import BasePage


class MembersPage(BasePage):

    LINK_VIEW_ID_PREFIX = "link-view-"
    BUTTON_ADD_A_MEMBER_ID = "button-add-a-member"

    def click_view_member_link(self, email: str):
        self.driver.find_element_by_id(self.LINK_VIEW_ID_PREFIX + email).click()

    def click_add_a_member_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_MEMBER_ID).click()

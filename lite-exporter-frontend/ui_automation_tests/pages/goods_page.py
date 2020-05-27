from ui_automation_tests.pages.BasePage import BasePage


class GoodsPage(BasePage):

    LINK_EDIT_ID = "link-edit"
    QUERY_TABLE_ID = "query_table"
    BUTTON_DELETE_GOOD_ID = "button-delete-good"

    def click_on_goods_edit_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_ID).click()

    def get_text_of_query_details(self):
        return self.driver.find_element_by_id(self.QUERY_TABLE_ID)

    def click_delete_button(self):
        self.driver.find_element_by_id(self.BUTTON_DELETE_GOOD_ID).click()

from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class GoodsPage(BasePage):

    # Selector for the edit/delete goods link in the table
    EDIT_LINK_ID = "edit"
    document_partial_id = "tr[id*='document']"
    QUERY_TABLE_ID = "query_table"
    GOOD_TABLE_ID = "good-details"

    # This is for the delete confirmation page
    DELETE_BUTTON = ".govuk-button--warning"

    def click_on_goods_edit_link(self):
        self.driver.find_element_by_id(self.EDIT_LINK_ID).click()

    def click_on_delete_link(self):
        self.driver.find_element_by_css_selector(self.DELETE_BUTTON).click()

    def get_text_of_product_details(self):
        return self.driver.find_element_by_id(self.GOOD_TABLE_ID).text

    def get_text_of_query_details(self):
        return self.driver.find_element_by_id(self.QUERY_TABLE_ID)

    def confirm_delete(self):
        functions.click_submit(self.driver)

    def get_text_of_document_added_item(self):
        return self.driver.find_element_by_css_selector(self.document_partial_id).text

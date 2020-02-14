from pages.shared import Shared
from shared.BasePage import BasePage


class GenericApplicationUltimateEndUsers(BasePage):

    BUTTON_ADD_ULTIMATE_RECIPIENT_ID = "button-add-ultimate-recipient"
    RADIO_DELETE_DOCUMENT_CONFIRM_YES_ID = "delete_document_confirmation-yes"
    LINK_DELETE_DOCUMENT_ID = "document_delete"
    LINK_ATTACH_DOCUMENT_ID = "attach_doc"
    TABLE_BODY = "tbody"
    TABLE_ROW = "tr"

    def get_ultimate_recipients(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_BODY + " " + self.TABLE_ROW)

    def click_add_ultimate_recipient_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_ULTIMATE_RECIPIENT_ID).click()

    def click_confirm_delete_yes(self):
        self.driver.find_element_by_id(self.RADIO_DELETE_DOCUMENT_CONFIRM_YES_ID).click()

    def click_delete_document_link(self, row):
        Shared(self.driver).get_table_row(row).find_element_by_id(self.LINK_DELETE_DOCUMENT_ID).click()

    def click_attach_document_link(self, row):
        attach_document_link = Shared(self.driver).get_table_row(row).find_element_by_id(self.LINK_ATTACH_DOCUMENT_ID)
        self.driver.execute_script("arguments[0].click();", attach_document_link)

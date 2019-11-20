from pages.shared import Shared
from shared.BasePage import BasePage


class ThirdPartyListPage(BasePage):
    GOVUK_BUTTON = ".govuk-button"  # CSS
    DELETE_DOCUMENT_LINK = "document_delete"  # ID
    DELETE_DOCUMENT_CONFIRM_YES = "delete_document_confirmation-yes"  # ID
    ATTACH_DOCUMENT = "attach_doc"  # ID

    def click_on_add_a_third_party(self):
        self.driver.find_element_by_css_selector(self.GOVUK_BUTTON).click()

    def click_on_delete_document(self, row):
        shared = Shared(self.driver)
        shared.get_table_row(row).find_element_by_id(self.DELETE_DOCUMENT_LINK).click()

    def accept_delete_confirm(self):
        self.driver.find_element_by_id(self.DELETE_DOCUMENT_CONFIRM_YES).click()

    def click_on_attach_document(self, row):
        shared = Shared(self.driver)

        attach_document_link = shared.get_table_row(row).find_element_by_id(self.ATTACH_DOCUMENT)
        self.driver.execute_script("arguments[0].click();", attach_document_link)

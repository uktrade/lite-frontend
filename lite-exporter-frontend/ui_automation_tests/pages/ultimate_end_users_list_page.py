from pages.shared import Shared


class ThirdPartyListPage:

    def __init__(self, driver):
        self.driver = driver
        self.govuk_button = ".govuk-button"  # CSS
        self.delete_document_link = "document_delete"  # ID
        self.delete_document_confirm_yes = "delete_document_confirmation-yes"  # ID
        self.attach_document = "attach_doc"  # ID

    def click_on_add_a_third_party(self):
        self.driver.find_element_by_css_selector(self.govuk_button).click()

    def click_on_delete_document(self, row):
        shared = Shared(self.driver)
        shared.get_table_row(row).find_element_by_id(self.delete_document_link).click()

    def accept_delete_confirm(self):
        self.driver.find_element_by_id(self.delete_document_confirm_yes).click()

    def click_on_attach_document(self, row):
        shared = Shared(self.driver)

        attach_document_link = shared.get_table_row(row).find_element_by_id(self.attach_document)
        self.driver.execute_script("arguments[0].click();", attach_document_link)

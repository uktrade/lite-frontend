from shared.BasePage import BasePage

from ui_automation_tests.pages.shared import Shared


class ApplicationPage(BasePage):

    BUTTON_WITHDRAW_APPLICATION_ID = "button-withdraw-application"
    BUTTON_SURRENDER_APPLICATION_ID = "button-surrender-application"
    BUTTON_EDIT_APPLICATION_ID = "button-edit-application"
    BUTTON_COPY_APPLICATION_ID = "button-copy-application"
    LABEL_APPLICATION_STATUS_ID = "label-application-status"
    LINK_NOTES_TAB_ID = "link-case-notes"  # ID
    LINK_ACTIVITY_TAB_ID = "link-activity"  # ID
    LINK_ECJU_QUERY_TAB_ID = "link-ecju-queries"  # ID
    LINK_GENERATED_DOCUMENTS_TAB_ID = "link-generated-documents"  # ID
    LINK_GENERATED_DOCUMENT_DOWNLOAD_LINK = "generated-document-download"  # ID
    ECJU_QUERY_RESPONSE_TEXT = "Respond to query"  # text
    ECJU_QUERIES_CLOSED = "closed-ecju-query"  # ID
    LINK_EDIT_APPLICATION = "a[href*='/edit-type/']"
    AUDIT_TRAIL_ITEM = ".app-activity__item"  # CSS

    def click_withdraw_application_button(self):
        self.driver.find_element_by_id(self.BUTTON_WITHDRAW_APPLICATION_ID).click()

    def click_surrender_application_button(self):
        self.driver.find_element_by_id(self.BUTTON_SURRENDER_APPLICATION_ID).click()

    def click_edit_application_link(self):
        self.driver.find_element_by_css_selector(self.LINK_EDIT_APPLICATION).click()

    def click_copy_application(self):
        self.driver.find_element_by_id(self.BUTTON_COPY_APPLICATION_ID).click()

    def click_ecju_query_tab(self):
        self.driver.find_element_by_id(self.LINK_ECJU_QUERY_TAB_ID).click()

    def click_generated_documents_tab(self):
        self.driver.find_element_by_id(self.LINK_GENERATED_DOCUMENTS_TAB_ID).click()

    def generated_documents_notification_count(self):
        return (
            self.driver.find_element_by_id(self.LINK_GENERATED_DOCUMENTS_TAB_ID)
            .find_element_by_css_selector(Shared.NOTIFICATION)
            .text
        )

    def generated_documents_count(self):
        return len(self.driver.find_elements_by_id(self.LINK_GENERATED_DOCUMENT_DOWNLOAD_LINK))

    def click_notes_tab(self):
        self.driver.find_element_by_id(self.LINK_NOTES_TAB_ID).click()

    def click_activity_tab(self):
        self.driver.find_element_by_id(self.LINK_ACTIVITY_TAB_ID).click()

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ECJU_QUERIES_CLOSED))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ECJU_QUERY_RESPONSE_TEXT + '")]'
        self.driver.find_elements_by_xpath(response)[no].click()

    def find_edit_application_button(self):
        return self.driver.find_elements_by_id(self.BUTTON_EDIT_APPLICATION_ID)

    def get_status(self):
        return self.driver.find_element_by_id(self.LABEL_APPLICATION_STATUS_ID).text

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)[no].text

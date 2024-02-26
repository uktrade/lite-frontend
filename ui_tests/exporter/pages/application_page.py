from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from ui_tests.exporter.pages.BasePage import BasePage
from ui_tests.exporter.pages.shared import Shared


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
    ECJU_QUERIES_OPEN = "open-ecju-query"  # ID
    ECJU_QUERIES_CLOSED = "closed-ecju-query"  # ID
    LINK_EDIT_APPLICATION = "a[href*='/edit-type/']"
    AUDIT_TRAIL_ITEM = ".app-activity__item"  # CSS
    CASE_BUTTONS = ".lite-app-bar__controls"  # CSS
    DRAFT_TAB = "applications-tab-draft"  # ID

    def click_withdraw_application_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_WITHDRAW_APPLICATION_ID).click()

    def click_surrender_application_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_SURRENDER_APPLICATION_ID).click()

    def click_edit_application_link(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.LINK_EDIT_APPLICATION).click()

    def click_copy_application(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_COPY_APPLICATION_ID).click()

    def notes_notification_count(self):
        return (
            self.driver.find_element(by=By.ID, value=self.LINK_NOTES_TAB_ID)
            .find_element(by=By.CSS_SELECTOR, value=Shared.NOTIFICATION)
            .text.strip()
        )

    def get_text_of_case_note(self, no):
        return self.driver.find_elements(by=By.CLASS_NAME, value="lite-application-note")[no].text

    def click_ecju_query_tab(self):
        self.driver.find_element(by=By.ID, value=self.LINK_ECJU_QUERY_TAB_ID).click()

    def ecju_query_notification_count(self):
        return (
            self.driver.find_element(by=By.ID, value=self.LINK_ECJU_QUERY_TAB_ID)
            .find_element(by=By.CSS_SELECTOR, value=Shared.NOTIFICATION)
            .text.strip()
        )

    def ecju_query_does_not_have_notifications(self):
        try:
            element_not_visible = WebDriverWait(self.driver, 10).until(
                expected_conditions.invisibility_of_element_located(
                    (By.CSS_SELECTOR, f"#{self.LINK_ECJU_QUERY_TAB_ID} {Shared.NOTIFICATION}")
                )
            )
            return element_not_visible
        except TimeoutException:
            print(f"Element with class {Shared.NOTIFICATION} remained visible throughout the time frame")

    def click_generated_documents_tab(self):
        self.driver.find_element(by=By.ID, value=self.LINK_GENERATED_DOCUMENTS_TAB_ID).click()

    def generated_documents_notification_count(self):
        return (
            self.driver.find_element(by=By.ID, value=self.LINK_GENERATED_DOCUMENTS_TAB_ID)
            .find_element(by=By.CSS_SELECTOR, value=Shared.NOTIFICATION)
            .text
        )

    def generated_documents_count(self):
        return len(self.driver.find_elements_by_id(self.LINK_GENERATED_DOCUMENT_DOWNLOAD_LINK))

    def click_notes_tab(self):
        self.driver.find_element(by=By.ID, value=self.LINK_NOTES_TAB_ID).click()

    def click_activity_tab(self):
        self.driver.find_element(by=By.ID, value=self.LINK_ACTIVITY_TAB_ID).click()

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ECJU_QUERIES_CLOSED))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ECJU_QUERY_RESPONSE_TEXT + '")]'
        self.driver.find_elements(by=By.XPATH, value=response)[no].click()

    def find_edit_application_button(self):
        return self.driver.find_elements_by_id(self.BUTTON_EDIT_APPLICATION_ID)

    def get_status(self):
        return self.driver.find_element(by=By.ID, value=self.LABEL_APPLICATION_STATUS_ID).text

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)[no].text

    def get_text_of_case_buttons(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.CASE_BUTTONS).text

    def click_draft_applications_tab(self):
        self.driver.find_element(by=By.ID, value=self.DRAFT_TAB).click()

    def get_open_queries_text(self):
        return self.driver.find_element(by=By.ID, value=self.ECJU_QUERIES_OPEN).text

    def get_closed_queries_text(self):
        return self.driver.find_element(by=By.ID, value=self.ECJU_QUERIES_CLOSED).text

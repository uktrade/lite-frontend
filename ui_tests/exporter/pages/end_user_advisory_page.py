from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.shared import Shared
from ui_tests.exporter.pages.BasePage import BasePage
from tests_common import functions


class EndUserAdvisoryPage(BasePage):
    APPLY_FOR_ADVISORY = "apply"  # id
    TABLE_ROW = ".govuk-table__body .govuk-table__row:last-child"  # css
    CASE_NOTES_TAB = "link-case-notes"  # id
    ADVISORY_DETAILS_LINK = "advisory-details-link"  # id
    CASE_NOTE_CSS_SELECTOR = ".lite-application-note"
    NAME_FILTER_ID = "name"
    BUTTON_APPLY_FILTERS = "button-apply-filters"
    COPY_LINK_ID = "copy"

    def click_apply_for_advisories(self):
        self.driver.find_element(by=By.ID, value=self.APPLY_FOR_ADVISORY).click()

    def open_end_user_advisory(self, end_user_advisory_id):
        self.driver.find_element(by=By.ID, value=end_user_advisory_id).find_element(
            by=By.ID, value=self.ADVISORY_DETAILS_LINK
        ).click()

    def case_note_notification_bubble_text(self):
        return (
            self.driver.find_element(by=By.ID, value=self.CASE_NOTES_TAB)
            .find_element(by=By.CSS_SELECTOR, value=Shared.NOTIFICATION)
            .text
        )

    def latest_case_note_text(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.CASE_NOTE_CSS_SELECTOR).text

    def filter_by_name(self, description: str):
        functions.try_open_filters(self.driver)
        self.driver.find_element(by=By.ID, value=self.NAME_FILTER_ID).clear()
        self.driver.find_element(by=By.ID, value=self.NAME_FILTER_ID).send_keys(description)
        self.driver.find_element(by=By.ID, value=self.BUTTON_APPLY_FILTERS).click()

    def get_row_text(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.TABLE_ROW).text

    def row_notifications(self):
        return (
            self.driver.find_element(by=By.CSS_SELECTOR, value=self.TABLE_ROW)
            .find_element(by=By.CSS_SELECTOR, value=Shared.NOTIFICATION)
            .text.split("\n")[0]
        )

    def click_row_copy(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.TABLE_ROW).find_element(
            by=By.ID, value=self.COPY_LINK_ID
        ).click()

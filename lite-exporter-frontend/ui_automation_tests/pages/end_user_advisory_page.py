from core.builtins.custom_tags import reference_code
from shared.BasePage import BasePage
from shared.tools import helpers
from pages.shared import Shared


class EndUserAdvisoryPage(BasePage):

    APPLY_FOR_ADVISORY = "apply"  # id
    TABLE_ROW = ".govuk-table__row"  # css
    CASE_NOTES_TAB = "link-case-notes"  # id
    NOTIFICATION_BUBBLE = ".lite-notification-bubble"  # css
    CASE_NOTE = ".lite-application-note"  # css

    def click_apply_for_advisories(self):
        self.driver.find_element_by_id(self.APPLY_FOR_ADVISORY).click()

    def open_advisory_by_reference_code(self, id):
        elements, no = self.get_table_rows_and_position(id)
        elements[no].find_elements_by_css_selector("a")[0].click()

    def confirm_advisory_displayed_by_reference_code(self, id):
        elements, no = self.get_table_rows_and_position(id)
        return elements[no].find_element_by_css_selector(Shared(self.driver).NOTIFICATION).is_displayed()

    def get_table_rows_and_position(self, id):
        elements = self.driver.find_elements_by_css_selector(self.TABLE_ROW)
        no = helpers.get_element_index_by_text(elements, reference_code(id), complete_match=False)
        return elements, no

    def case_note_notification_bubble_text(self):
        tab = self.driver.find_element_by_id(self.CASE_NOTES_TAB)
        return tab.find_element_by_css_selector(self.NOTIFICATION_BUBBLE).text

    def latest_case_note_text(self):
        return self.driver.find_elements_by_css_selector(".lite-application-note")[0].text

from core.builtins.custom_tags import reference_code
from ui_automation_tests.helpers import helpers
from ui_automation_tests.pages.shared import Shared


class EndUserAdvisoryPage:

    def __init__(self, driver):
        self.driver = driver

        self.apply_for_advisory = "apply"  # id
        self.table_row = ".govuk-table__row"  # css
        self.case_notes_tab = "case-notes-tab"  # id
        self.notification_bubble = ".lite-notification-bubble"  # css
        self.case_note = ".lite-application-note"  # css

    def click_apply_for_advisories(self):
        self.driver.find_element_by_id(self.apply_for_advisory).click()

    def open_advisory_by_reference_code(self, id):
        elements, no = self.get_table_rows_and_position(id)
        elements[no].find_elements_by_css_selector("a")[0].click()

    def confirm_advisory_displayed_by_reference_code(self, id):
        elements, no = self.get_table_rows_and_position(id)
        return elements[no].find_element_by_css_selector(Shared(self.driver).notification).is_displayed()

    def get_table_rows_and_position(self, id):
        elements = self.driver.find_elements_by_css_selector(self.table_row)
        no = helpers.get_element_index_by_partial_text(elements, reference_code(id))
        return elements, no

    def case_note_notification_bubble_text(self):
        tab = self.driver.find_element_by_id(self.case_notes_tab)
        return tab.find_element_by_css_selector(self.notification_bubble).text

    def latest_case_note_text(self):
        return self.driver.find_elements_by_css_selector(".lite-application-note")[0].text

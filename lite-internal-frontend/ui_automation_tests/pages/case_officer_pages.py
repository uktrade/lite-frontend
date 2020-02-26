from shared.BasePage import BasePage

from ui_automation_tests.shared import functions


class CaseOfficerPages(BasePage):
    BUTTON_ASSIGN_ID = "button-assign"  # id
    BUTTON_UNASSIGN_ID = "button-unassign"  # id
    CHOICES_NAMES = ".govuk-radios__item label"
    CURRENT_CASE_OFFICER_PANEL = ".govuk-grid-column-one-third .lite-related-items"
    TEXTAREA_SEARCH_ID = "input-search"  # id
    BUTTON_SEARCH_ID = "button-search"  # id
    RADIO_BUTTON = "input[name='user']"

    def select_first_user(self):
        self.driver.find_elements_by_css_selector(self.RADIO_BUTTON)[0].click()

    def click_assign(self):
        self.driver.find_element_by_id(self.BUTTON_ASSIGN_ID).click()

    def click_unassign(self):
        self.driver.find_element_by_id(self.BUTTON_UNASSIGN_ID).click()

    def search(self, text):
        self.driver.find_element_by_id(self.TEXTAREA_SEARCH_ID).send_keys(text)
        self.driver.find_element_by_id(self.BUTTON_SEARCH_ID).click()

    def get_users_name(self):
        return self.driver.find_elements_by_css_selector(self.CHOICES_NAMES)

    def is_current_case_officer(self):
        return functions.element_with_css_selector_exists(self.driver, self.CURRENT_CASE_OFFICER_PANEL)

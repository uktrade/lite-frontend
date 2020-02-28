from shared.BasePage import BasePage

from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id


class CaseOfficerPages(BasePage):
    BUTTON_ASSIGN_ID = "button-assign"  # id
    BUTTON_UNASSIGN_ID = "button-unassign"  # id
    VISIBLE_CHOICES_EMAILS = ".govuk-radios__item.visible .govuk-hint"
    VISIBLE_CHOICE_BUTTON = ".govuk-radios__item.visible .govuk-radios__input"
    CURRENT_CASE_OFFICER_PANEL = ".govuk-grid-column-one-third .lite-related-items"
    CURRENT_CASE_OFFICER_LINK_ID = "selected-case-officer"
    TEXTAREA_SEARCH_ID = "filter-box"

    def select_first_user(self):
        self.driver.find_element_by_css_selector(self.VISIBLE_CHOICE_BUTTON).click()

    def click_unassign(self):
        scroll_to_element_by_id(self.driver, self.BUTTON_UNASSIGN_ID)
        self.driver.find_element_by_id(self.BUTTON_UNASSIGN_ID).click()

    def search(self, text):
        self.driver.find_element_by_id(self.TEXTAREA_SEARCH_ID).send_keys(text)

    def get_users_email(self):
        return self.driver.find_elements_by_css_selector(self.VISIBLE_CHOICES_EMAILS)

    def get_current_case_officer(self):
        return self.driver.find_element_by_id(self.CURRENT_CASE_OFFICER_LINK_ID).text

import helpers.helpers as utils
from helpers.BasePage import BasePage


class CaseListPage(BasePage):

    # Table
    CASES_TABLE_ROW = '.lite-cases-table-row'  # CSS
    CHECKBOX_CASE = ".govuk-checkboxes__input[value='"  # CSS
    CHECKBOX_TEXT = ".govuk-checkboxes"  # CSS
    CHECKBOX_SELECT_ALL = "select-all-checkbox"  # ID

    # App Bar Buttons
    BUTTON_ASSIGN_USERS = "assign-users-button"  # ID

    # Filters
    BUTTON_APPLY_FILTERS = 'button-apply-filters'  # ID
    BUTTON_CLEAR_FILTERS = 'button-clear-filters'  # ID
    LINK_SHOW_FILTERS = 'show-filters-link'  # ID
    LINK_HIDE_FILTERS = 'hide-filters-link'  # ID
    FILTER_BAR = 'lite-filter-bar--horizontal'  # Class

    # Deprecated
    FILTER_SEARCH_BOX = "filter-box"  # ID
    assignee = "[style='margin-bottom: 6px;']"  # CSS
    no_assignee = "[style='margin-bottom: 0; opacity: .7;']"  # CSS

    def click_on_case_checkbox(self, case_id):
        self.driver.find_element_by_css_selector(self.CHECKBOX_CASE + case_id + "']").click()

    def click_on_assign_users_button(self):
        self.driver.find_element_by_id(self.BUTTON_ASSIGN_USERS).click()

    def get_text_of_assignees(self, case_id):
        return self.driver.find_element_by_xpath("//*[text()[contains(.,'" + case_id + "')]]/following::p/following::p").text

    def click_select_all_checkbox(self):
        self.driver.find_element_by_id(self.CHECKBOX_SELECT_ALL).click()

    def get_class_name_of_assign_users_button(self):
        return self.driver.find_element_by_id(self.BUTTON_ASSIGN_USERS).get_attribute('class')

    def enter_name_to_filter_search_box(self, name):
        return self.driver.find_element_by_id(self.FILTER_SEARCH_BOX).send_keys(name)

    def get_text_checkbox_elements(self):
        return self.driver.find_elements_by_css_selector(self.CHECKBOX_TEXT)

    def assert_case_is_present(self, case_id):
        elements = self.driver.find_elements_by_css_selector(self.CASES_TABLE_ROW)
        no = utils.get_element_index_by_partial_text(elements, case_id)
        return elements[no].is_displayed()

    def click_apply_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTERS).click()

    def click_clear_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_CLEAR_FILTERS).click()

    def click_show_filters_link(self):
        self.driver.find_element_by_id(self.LINK_SHOW_FILTERS).click()

    def click_hide_filters_link(self):
        self.driver.find_element_by_id(self.LINK_HIDE_FILTERS).click()

    def is_filters_visible(self):
        return self.driver.find_element_by_class_name(self.FILTER_BAR).is_displayed()

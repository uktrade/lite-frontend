class CaseListPage():

    def __init__(self, driver):
        self.driver = driver
        self.select_all_checkbox = "select-all-checkbox"  # id
        self.case_checkbox = ".govuk-checkboxes__input[value='"  # css
        self.checkbox_text = ".govuk-checkboxes"  # css
        self.assign_users_button = "assign-users-button"  # id
        self.assignee = "[style='margin-bottom: 6px;']"  # css
        self.no_assignee = "[style='margin-bottom: 0; opacity: .7;']"  # css
        self.filter_search_box = "filter-box"  # id

    def click_on_case_checkbox(self, case_id):
        self.driver.find_element_by_css_selector(self.case_checkbox + case_id + "']").click()

    def click_on_assign_users_button(self):
        self.driver.find_element_by_id(self.assign_users_button).click()

    def get_text_of_assignees(self, case_id):
        return self.driver.find_element_by_xpath("//*[text()[contains(.,'" + case_id + "')]]/following::p/following::p").text

    def click_select_all_checkbox(self):
        self.driver.find_element_by_id(self.select_all_checkbox).click()

    def get_class_name_of_assign_users_button(self):
        return self.driver.find_element_by_id(self.assign_users_button).get_attribute('class')

    def enter_name_to_filter_search_box(self, name):
        return self.driver.find_element_by_id(self.filter_search_box).send_keys(name)

    def get_text_checkbox_elements(self):
        return self.driver.find_elements_by_css_selector(self.checkbox_text)

    def assert_case_is_present(self, case_id):
        case_row = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + case_id + "')]]")
        return case_row.is_displayed()

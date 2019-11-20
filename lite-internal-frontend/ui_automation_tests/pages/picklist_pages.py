from helpers.BasePage import BasePage


class PicklistPages(BasePage):
    PICKLIST_TAB = '.lite-tabs__tab[href*="picklists"]'  # css
    PICKLIST_EDIT_BUTTON = '.govuk-button[href*="edit"]'  # css
    PICKLIST_ADD_BUTTON = '.govuk-button[href*="add"]'  # css
    PICKLIST_DEACTIVATE_BUTTON = '.govuk-button[href*="deactivate"]'  # css
    PICKLIST_REACTIVATE_BUTTON = '.govuk-button[href*="reactivate"]'  # css
    PICKLIST_TYPE_SUB_NAV = '.govuk-link[href*="type='  # css
    PICKLIST_PAGE_BODY = ".govuk-main-wrapper"  # css
    PICKLIST_NAME_FIELD = "name"  # name
    PICKLIST_DESCRIPTION_FIELD = "text"  # name
    PICKLIST_NAMES_IN_LIST = "h4 a"  # css
    PICKLIST_LIST_NAME = ".govuk-heading-s"  # css
    PICKLIST_LIST_DESCRIPTION = ".app-picklist-item__text"  # css
    ERRORS = ".govuk-error-summary__list"  # css
    CONTEXT_SUGGESTIONS_OVERLAY = ".tribute-container"  # css
    CONTEXT_SUGGESTION = ".tribute-container .highlight"  # css

    def click_on_picklist_tab(self):
        self.driver.find_element_by_css_selector(self.PICKLIST_TAB).click()

    def click_on_picklist_edit_button(self):
        self.driver.find_element_by_css_selector(self.PICKLIST_EDIT_BUTTON).click()

    def click_on_picklist_deactivate_button(self):
        self.driver.find_element_by_css_selector(self.PICKLIST_DEACTIVATE_BUTTON).click()

    def click_on_picklist_reactivate_button(self):
        self.driver.find_element_by_css_selector(self.PICKLIST_REACTIVATE_BUTTON).click()

    def click_on_picklist_type_sub_nav(self, type):
        self.driver.find_element_by_css_selector(self.PICKLIST_TYPE_SUB_NAV + type + '"]').click()

    def click_on_picklist_add_button(self):
        self.driver.find_element_by_css_selector(self.PICKLIST_ADD_BUTTON).click()

    def get_text_of_picklist_page_body(self):
        return self.driver.find_element_by_css_selector(self.PICKLIST_PAGE_BODY).text

    def get_latest_picklist_name(self):
        return self.driver.find_elements_by_css_selector(self.PICKLIST_LIST_NAME)[0].text

    def get_latest_picklist_description(self):
        return self.driver.find_elements_by_css_selector(self.PICKLIST_LIST_DESCRIPTION)[0].text

    def type_into_picklist_name(self, name):
        self.driver.find_element_by_name(self.PICKLIST_NAME_FIELD).send_keys(name)

    def type_into_picklist_description(self, description):
        self.driver.find_element_by_name(self.PICKLIST_DESCRIPTION_FIELD).send_keys(description)

    def clear_picklist_name_and_description(self):
        self.driver.find_element_by_name(self.PICKLIST_NAME_FIELD).clear()
        self.driver.find_element_by_name(self.PICKLIST_DESCRIPTION_FIELD).clear()

    def get_elements_of_picklist_names_in_list(self):
        return self.driver.find_elements_by_css_selector(self.PICKLIST_NAMES_IN_LIST)

    def context_suggestions_are_displayed(self):
        return self.driver.find_element_by_css_selector(self.CONTEXT_SUGGESTIONS_OVERLAY).is_displayed()

    def get_context_suggestion_variable_name(self):
        return self.driver.find_element_by_css_selector(self.CONTEXT_SUGGESTIONS_OVERLAY).text

    def click_context_suggestion(self):
        self.driver.find_element_by_css_selector(self.CONTEXT_SUGGESTION).click()

    def get_errors(self):
        return self.driver.find_element_by_css_selector(self.ERRORS).text

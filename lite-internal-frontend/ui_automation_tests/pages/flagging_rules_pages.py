from selenium.webdriver.support.select import Select
from shared.BasePage import BasePage

from ui_automation_tests.shared import functions


class FlaggingRulePages(BasePage):
    RADIO_BTN_FLAGGING_RULE_TYPE_ID = "level"
    GOOD_OPTION_ID = RADIO_BTN_FLAGGING_RULE_TYPE_ID + "-Good"
    DESTINATION_OPTION_ID = RADIO_BTN_FLAGGING_RULE_TYPE_ID + "-Destination"
    CASE_OPTION_ID = RADIO_BTN_FLAGGING_RULE_TYPE_ID + "-Case"
    MATCHING_VALUE_ID = "matching_value"
    SELECT_FLAG_ID = "flag"
    BTN_CREATE_NEW_FLAGGING_RULE = "add-a-flag-button"
    INCLUDE_DEACTIVATED = "Include deactivated"
    BUTTON_APPLY_FILTERS_ID = "button-apply-filters"
    REACTIVATE_FLAG_BUTTON = "a[href*='/Active/']"  # CSS
    DEACTIVATE_FLAG_BUTTON = "a[href*='/Deactivated/']"  # CSS
    CONFIRM_DEACTIVATE_DEACTIVATE = "confirm-yes"

    def click_include_deactivated(self):
        self.driver.find_element_by_id(self.INCLUDE_DEACTIVATED).click()

    def click_apply_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTERS_ID).click()

    def create_new_flagging_rule(self):
        self.driver.find_element_by_id(self.BTN_CREATE_NEW_FLAGGING_RULE).click()

    def select_flagging_rule_type(self, type):
        if type == "Good":
            self.driver.find_element_by_id(self.GOOD_OPTION_ID).click()
        elif type == "Destination":
            self.driver.find_element_by_id(self.DESTINATION_OPTION_ID).click()
        elif type == "Case":
            self.driver.find_element_by_id(self.CASE_OPTION_ID).click()

    def enter_control_list(self, text):
        self.driver.find_element_by_id(self.MATCHING_VALUE_ID).clear()
        self.driver.find_element_by_id(self.MATCHING_VALUE_ID).send_keys(text)

    def select_flag(self, flag):
        select = Select(self.driver.find_element_by_id(self.SELECT_FLAG_ID))
        select.select_by_visible_text(flag)

    def enter_country(self, country):
        functions.send_keys_to_autocomplete(self.driver, self.MATCHING_VALUE_ID, country)

    def select_case_type(self, case_type):
        select = Select(self.driver.find_element_by_id(self.MATCHING_VALUE_ID))
        select.select_by_value(case_type)

    def click_on_deactivate_flag(self, element):
        element.find_element_by_css_selector(self.DEACTIVATE_FLAG_BUTTON).click()

    def click_confirm_deactivate_activate(self):
        self.driver.find_element_by_id(self.CONFIRM_DEACTIVATE_DEACTIVATE).click()

    def click_on_reactivate_flag(self):
        self.driver.find_element_by_css_selector(self.REACTIVATE_FLAG_BUTTON).click()

from selenium.webdriver.support.select import Select

from shared import selectors
from shared.BasePage import BasePage

from ui_automation_tests.shared import functions


class RoutingRulesPage(BasePage):
    TEXT_TIER_ID = "tier"
    TEXT_QUEUE_ID = "queue"
    TEXT_COUNTRY_ID = "country"
    SELECT_CASE_STATUS_ID = "status"
    BTN_CREATE_NEW_ROUTING_RULE_ID = "create-routing-rule"
    EDIT_ROUTING_RULE_BUTTON_ID = "edit"
    REACTIVATE_ROUTING_RULE_BUTTON_ID = "reactivate"
    DEACTIVATE_ROUTING_RULE_BUTTON_ID = "deactivate"
    CONFIRM_DEACTIVATE_REACTIVATE = "confirm-yes"
    CHECKBOX_ADDITIONAL_RULES = "input[name='additional_rules[]'][type='checkbox']"  # CSS
    SELECT_FLAG_ID = "flag"
    CHECKBOX_AND_LABEL = ".govuk-checkboxes__item"
    RADIO_BUTTONS = ".govuk-radios__input"
    TEAM_ID_PREFIX = "team-"

    def create_new_routing_rule(self):
        self.driver.find_element_by_id(self.BTN_CREATE_NEW_ROUTING_RULE_ID).click()

    def initial_details_form(self, case_status=None, queue=None, tier=None, additional_rules=None):
        if case_status:
            self.select_case_status(case_status)

        if queue:
            self.enter_queue(queue)

        if tier:
            self.enter_tier(tier)

        if additional_rules:
            self.select_all_additional_rules()
        else:
            self.select_no_additional_rules()

    def select_all_additional_rules(self):
        rules = self._get_rules()
        for rule in rules:
            if not rule.is_selected():
                rule.click()

    def select_no_additional_rules(self):
        rules = self._get_rules()
        for rule in rules:
            if rule.is_selected():
                rule.click()

    def _get_rules(self):
        rules = self.driver.find_elements_by_css_selector(self.CHECKBOX_ADDITIONAL_RULES)
        assert len(rules) == 4, "expecting 4 options to be selectable"
        return rules

    def enter_queue(self, text):
        functions.send_keys_to_autocomplete(self.driver, self.TEXT_QUEUE_ID, text)

    def select_case_status(self, status):
        select = Select(self.driver.find_element_by_id(self.SELECT_CASE_STATUS_ID))
        select.select_by_visible_text(status)

    def enter_tier(self, text):
        self.driver.find_element_by_id(self.TEXT_TIER_ID).clear()
        self.driver.find_element_by_id(self.TEXT_TIER_ID).send_keys(text)

    def select_case_type_by_text(self, text):
        self.driver.find_element_by_id(text).click()

    def select_flag(self, flag_name):
        self.driver.find_element_by_id(flag_name.replace(" ", "-")).click()

    def enter_country(self, country):
        functions.send_keys_to_autocomplete(self.driver, self.TEXT_COUNTRY_ID, country)

    def select_first_user(self):
        self.driver.find_element_by_css_selector(self.RADIO_BUTTONS).click()

    def click_on_deactivate_rule(self, element):
        element.find_element_by_id(self.DEACTIVATE_ROUTING_RULE_BUTTON_ID).click()

    def click_on_reactivate_rule(self, element):
        element.find_element_by_id(self.REACTIVATE_ROUTING_RULE_BUTTON_ID).click()

    def click_confirm_deactivate_activate(self):
        self.driver.find_element_by_id(self.CONFIRM_DEACTIVATE_REACTIVATE).click()

    def find_row_by_queue_id(self, queue_id):
        # the queue_id is assigned to a td, and we need the tr, so xpath is used to get the parent element.
        return self.driver.find_element_by_id(queue_id).find_element_by_xpath("..")

    def edit_row_by_queue_id(self, queue_id):
        self.find_row_by_queue_id(queue_id).find_element_by_id(self.EDIT_ROUTING_RULE_BUTTON_ID).click()

    def select_team(self, team_id):
        self.driver.find_element_by_id(self.TEAM_ID_PREFIX + team_id).click()

    def filter_by_queue_name(self, queue_name):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id("queue").send_keys(queue_name)
        self.driver.find_element_by_css_selector(selectors.BUTTON_APPLY_FILTERS).click()

import time
from pages.shared import Shared
from shared import selectors
from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id


class CaseTabs:
    DETAILS = "details"
    USER_ADVICE = "user-advice"
    TEAM_ADVICE = "team-advice"
    FINAL_ADVICE = "final-advice"
    ADDITIONAL_CONTACTS = "additional-contacts"
    ECJU_QUERIES = "ecju-queries"
    DOCUMENTS = "documents"
    ACTIVITY = "activity"


class CasePage(BasePage):
    TABLE_GOODS_ID = "table-goods"
    TABLE_DESTINATIONS_ID = "table-destinations"
    TABLE_DELETED_ENTITIES_ID = "table-inactive-entities"

    BUTTON_RERUN_ROUTING_RULES_ID = "button-rerun-routing-rules"
    BUTTON_SET_GOODS_FLAGS_ID = "button-edit-goods-flags"
    BUTTON_SET_DESTINATIONS_FLAGS_ID = "button-edit-destinations-flags"

    LINK_CHANGE_STATUS_ID = "link-change-status"
    LINK_CHANGE_CASE_FLAGS_ID = "link-change-flags"
    LINK_ASSIGN_CASE_OFFICER_ID = "link-change-case-officer"
    LINK_ASSIGN_USERS_ID = "link-change-assigned-users"

    def change_tab(self, tab: str):
        if tab == CaseTabs.USER_ADVICE or tab == CaseTabs.TEAM_ADVICE or tab == CaseTabs.FINAL_ADVICE:
            self.driver.find_element_by_id("tab-collection-advice").click()
        self.driver.find_element_by_id("tab-" + tab).click()

    def click_change_case_flags(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_CASE_FLAGS_ID).click()

    def click_assign_case_officer(self):
        scroll_to_element_by_id(self.driver, self.LINK_ASSIGN_CASE_OFFICER_ID)
        self.driver.find_element_by_id(self.LINK_ASSIGN_CASE_OFFICER_ID).click()

    def click_assign_users(self):
        scroll_to_element_by_id(self.driver, self.LINK_ASSIGN_USERS_ID)
        self.driver.find_element_by_id(self.LINK_ASSIGN_USERS_ID).click()

    def click_change_status(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_STATUS_ID).click()

    def click_rerun_routing_rules(self):
        self.driver.find_element_by_id(self.BUTTON_RERUN_ROUTING_RULES_ID).click()

    def get_goods(self):
        return self.driver.find_elements_by_css_selector(f"#{self.TABLE_GOODS_ID} {Shared(self.driver).TABLE_ROW_CSS}")

    def select_first_good(self):
        scroll_to_element_by_id(self.driver, self.TABLE_GOODS_ID)
        self.driver.find_element_by_css_selector(f"#{self.TABLE_GOODS_ID} {selectors.CHECKBOX}").click()

    def get_goods_text(self):
        return self.driver.find_element_by_id(self.TABLE_GOODS_ID).text

    def get_destinations(self):
        return self.driver.find_elements_by_css_selector(
            f"#{self.TABLE_DESTINATIONS_ID} {Shared(self.driver).TABLE_ROW_CSS}"
        )

    def get_destinations_text(self):
        return self.driver.find_element_by_id(self.TABLE_DESTINATIONS_ID).text

    def get_deleted_entities_text(self):
        return self.driver.find_element_by_id(self.TABLE_DELETED_ENTITIES_ID).text

    def select_destinations(self):
        for destination in self.driver.find_elements_by_css_selector(self.TABLE_DESTINATIONS_ID + selectors.CHECKBOX):
            destination.click()

    def is_flag_applied(self, flag_name):
        self.driver.find_element_by_id("candy-flags").click()
        # TODO Make this an implicit wait!
        time.sleep(0.5)
        return flag_name in self.driver.find_element_by_id("popup-flags").text

    def is_flag_in_applied_flags_list(self, flag_name):
        text = self.driver.find_element_by_id("checkbox-counter").text
        return flag_name in text

    def is_goods_flag_applied(self, flag_name):
        return flag_name in self.driver.find_element_by_id(self.TABLE_GOODS_ID).text

    def click_edit_goods_flags(self):
        self.driver.find_element_by_id(self.BUTTON_SET_GOODS_FLAGS_ID).click()

    def click_edit_destinations_flags(self):
        self.driver.find_element_by_id(self.BUTTON_SET_DESTINATIONS_FLAGS_ID).click()

    def select_destination(self, index):
        self.driver.find_elements_by_css_selector(f"#{self.TABLE_DESTINATIONS_ID} {selectors.CHECKBOX}")[index].click()

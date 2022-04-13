from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

from ui_tests.caseworker.pages.BasePage import BasePage
from ui_tests.caseworker.pages.shared import Shared
from tests_common import functions
from tests_common.tools.helpers import get_element_index_by_text, scroll_to_element_by_id


class CaseListPage(BasePage):
    # Table
    CASES_TABLE_ROW = ".govuk-table__row"  # CSS
    CHECKBOX_CASE = ".govuk-checkboxes__input[value='"  # CSS
    CHECKBOX_TEXT = ".govuk-checkboxes"  # CSS
    CHECKBOX_SELECT_ALL = "button-select-all"  # ID

    # App Bar Buttons
    BUTTON_ASSIGN_USERS = "assign-users-button"  # ID

    # Filters
    BUTTON_CLEAR_FILTERS = "button-clear-filters"  # ID
    LINK_ADVANCED_FILTERS = "advanced-filters-link"  # ID
    LINK_HIDE_FILTERS = "hide-filters-link"  # ID
    FILTER_BAR = "lite-filter-bar"  # Class
    USER_STATUS_DROPDOWN_ID = "status"
    STATUS_DROPDOWN = "status"  # ID
    CASE_TYPE_DROPDOWN = "case_type"  # ID
    INPUT_ASSIGNED_USER_ID = "assigned_user"
    FILTER_SEARCH_BOX = "filter-box"  # ID
    SHOW_TEAM_ECJU_AND_HIDDEN_CASES = "show-hidden-cases"
    QUEUE_SEARCH_BOX = "filter-queues"
    # Queue dropdown
    LINK_CHANGE_QUEUE_ID = "link-queue"

    # Advanced filters
    CASE_REFERENCE_ID = "case_reference"
    ORGANISATION_NAME_ID = "organisation_name"
    EXPORTER_APPLICATION_REFERENCE_ID = "exporter_application_reference"
    FINAL_ADVICE_TYPE_ID = "final_advice_type"
    TEAM_ADVICE_TYPE_ID = "team_advice_type"
    MAX_SLA_DAYS_REMAINING_ID = "max_sla_days_remaining"
    MIN_SLA_DAYS_REMAINING_ID = "min_sla_days_remaining"
    SUBMITTED_FROM_DAY_ID = "submitted_from_day"
    SUBMITTED_FROM_MONTH_ID = "submitted_from_month"
    SUBMITTED_FROM_YEAR_ID = "submitted_from_year"
    SUBMITTED_TO_DAY_ID = "submitted_to_day"
    SUBMITTED_TO_MONTH_ID = "submitted_to_month"
    SUBMITTED_TO_YEAR_ID = "submitted_to_year"
    PARTY_NAME_ID = "party_name"
    PARTY_ADDRESS_ID = "party_address"
    GOODS_RELATED_DESCRIPTION_ID = "goods_related_description"
    CONTROL_LIST_ENTRY_ID = "control_list_entry"

    ADVANCED_FILTERS = [
        CASE_REFERENCE_ID,
        ORGANISATION_NAME_ID,
        EXPORTER_APPLICATION_REFERENCE_ID,
        FINAL_ADVICE_TYPE_ID,
        TEAM_ADVICE_TYPE_ID,
        MAX_SLA_DAYS_REMAINING_ID,
        MIN_SLA_DAYS_REMAINING_ID,
        SUBMITTED_FROM_DAY_ID,
        SUBMITTED_FROM_MONTH_ID,
        SUBMITTED_FROM_YEAR_ID,
        SUBMITTED_TO_DAY_ID,
        SUBMITTED_TO_MONTH_ID,
        SUBMITTED_TO_YEAR_ID,
        PARTY_NAME_ID,
        PARTY_ADDRESS_ID,
        GOODS_RELATED_DESCRIPTION_ID,
        CONTROL_LIST_ENTRY_ID,
    ]

    # Notification for updated cases
    BANNER_EXPORTER_AMENDMENTS_ID = "banner-exporter-amendments"

    # SLA
    SLA_CLASS = "app-sla__container"

    # Enforcement
    EXPORT_ENFORCEMENT_XML_BUTTON_ID = "button-export-xml"

    def search_pages_for_id(self, id):
        is_present = len(self.driver.find_elements_by_link_text(id))
        number_of_pages = len(self.driver.find_elements_by_css_selector(".lite-pagination__item"))
        page_number = number_of_pages
        if number_of_pages != 0:
            while is_present == 0:
                url = self.driver.current_url
                if "page" not in url:
                    self.driver.find_element_by_id("page-" + str(number_of_pages)).click()
                else:
                    next_page = url + "&page=" + str(page_number)
                    self.driver.get(next_page)
                page_number -= 1
                is_present = len(self.driver.find_elements_by_link_text(id))

    def click_on_case(self, case_id):
        self.driver.find_element(by=By.ID, value=f"case-{case_id}").click()

    def click_on_case_checkbox(self, case_id):
        self.driver.find_element_by_css_selector(self.CHECKBOX_CASE + case_id + "']").click()

    def click_on_assign_users_button(self):
        self.driver.find_element_by_id(self.BUTTON_ASSIGN_USERS).click()

    def has_assignees(self, driver, case_id):
        elements = Shared(driver).get_rows_in_lite_table()
        no = get_element_index_by_text(elements, case_id)
        return len(elements[no].find_elements_by_css_selector(".app-assignments__container")) != 0

    def get_text_of_assignees(self, driver, case_id):
        elements = Shared(driver).get_rows_in_lite_table()
        no = get_element_index_by_text(elements, case_id)
        return elements[no].find_element_by_css_selector(".app-assignments__container").text

    def click_select_all_checkbox(self):
        self.driver.find_element_by_id(self.CHECKBOX_SELECT_ALL).click()

    def get_class_name_of_assign_users_button(self):
        return self.driver.find_element_by_id(self.BUTTON_ASSIGN_USERS).get_attribute("class")

    def get_text_checkbox_elements(self):
        return self.driver.find_elements_by_css_selector(self.CHECKBOX_TEXT)

    def assert_case_is_present(self, case_id):
        elements = self.driver.find_elements_by_css_selector(self.CASES_TABLE_ROW)
        no = get_element_index_by_text(elements, case_id, complete_match=False)
        return elements[no].is_displayed()

    def click_clear_filters_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_CLEAR_FILTERS).click()

    def click_advanced_filters_button(self):
        self.driver.find_element_by_id(self.LINK_ADVANCED_FILTERS).click()

    def click_hide_filters_link(self):
        self.driver.find_element_by_id(self.LINK_HIDE_FILTERS).click()

    def is_filters_visible(self):
        return self.driver.find_element_by_class_name(self.FILTER_BAR).is_displayed()

    def click_on_queue_title(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_QUEUE_ID).click()

    def search_for_queue(self, queue_name):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.QUEUE_SEARCH_BOX))
        )
        self.driver.find_element_by_id(self.QUEUE_SEARCH_BOX).send_keys(queue_name)

    def click_on_queue_name(self, queue_name):
        self.click_on_queue_title()
        self.search_for_queue(queue_name)
        self.driver.find_elements_by_css_selector('#queues .app-menu__item:not([style="display: none;"])')[0].click()

    def select_filter_status_from_dropdown(self, status):
        Select(self.driver.find_element_by_id(self.STATUS_DROPDOWN)).select_by_visible_text(status)

    def select_filter_user_status_from_dropdown(self, status):
        scroll_to_element_by_id(self.driver, self.USER_STATUS_DROPDOWN_ID)
        Select(self.driver.find_element_by_id(self.USER_STATUS_DROPDOWN_ID)).select_by_visible_text(status)

    def select_filter_case_type_from_dropdown(self, status):
        Select(self.driver.find_element(by=By.ID, value=self.CASE_TYPE_DROPDOWN)).select_by_visible_text(status)

    def click_on_exporter_amendments_banner(self):
        self.driver.find_element_by_id(self.BANNER_EXPORTER_AMENDMENTS_ID).click()

    def enter_assigned_user_filter_text(self, text):
        self.driver.find_element_by_id(self.INPUT_ASSIGNED_USER_ID).clear()
        functions.send_keys_to_autocomplete(self.driver, self.INPUT_ASSIGNED_USER_ID, text)

    def enter_name_to_filter_search_box(self, text):
        self.driver.find_element_by_id(self.FILTER_SEARCH_BOX).send_keys(text)

    def get_case_row(self, case_id):
        return self.driver.find_element(by=By.ID, value=case_id)

    def assert_all_advanced_filters_available(self):
        for advanced_filter in self.ADVANCED_FILTERS:
            assert self.driver.find_element_by_id(advanced_filter)

    def filter_by_exporter_application_reference(self, exporter_application_reference):
        self.driver.find_element_by_id(self.EXPORTER_APPLICATION_REFERENCE_ID).send_keys(exporter_application_reference)

    def filter_by_case_reference(self, case_reference):
        self.driver.find_element(by=By.ID, value=self.CASE_REFERENCE_ID).send_keys(case_reference)

    def filter_by_goods_related_description(self, goods_related_description):
        self.driver.find_element_by_id(self.GOODS_RELATED_DESCRIPTION_ID)
        self.driver.find_element_by_id(self.GOODS_RELATED_DESCRIPTION_ID).send_keys(goods_related_description)

    def filter_by_organisation_name(self, org_name):
        self.driver.find_element_by_id(self.ORGANISATION_NAME_ID)
        self.driver.find_element_by_id(self.ORGANISATION_NAME_ID).send_keys(org_name)

    def get_case_row_sla(self, row: WebElement):
        return row.find_element_by_class_name(self.SLA_CLASS).text

    def click_checkbox_to_show_team_ecju_query_and_hidden_cases(self):
        return self.driver.find_element_by_id(self.SHOW_TEAM_ECJU_AND_HIDDEN_CASES).click()

    def click_export_enforcement_xml(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.EXPORT_ENFORCEMENT_XML_BUTTON_ID))
        ).click()

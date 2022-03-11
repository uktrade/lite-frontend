import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests_common import functions
from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_by_id


class Shared(BasePage):

    SUBMIT_BUTTON = '.govuk-button[type*="submit"]'  # CSS
    ERROR_MESSAGE = ".govuk-error-message"  # CSS
    TABLE_CSS = ".govuk-table"  # CSS
    SUMMARY_LIST_CSS = ".govuk-summary-list"  # CSS
    TABLE_BODY_CSS = ".govuk-table__body"  # CSS
    TABLE_ROW_CSS = ".govuk-table__body .govuk-table__row"  # CSS
    TABLE_CELL_CSS = ".govuk-table__body .govuk-table__cell"  # CSS
    GOVUK_CAPTION = ".govuk-caption-l"  # CSS
    BODY = "body"  # CSS
    LINKS_IN_TABLE = ".govuk-table td a"
    ROWS_IN_CASES_TABLE = ".govuk-table__body .govuk-table__row"  # CSS
    LINKS_IN_LITE_TABLE = ".govuk-table__cell a"  # CSS
    SNACKBAR_SELECTOR = ".app-snackbar"
    LITE_NOTICE_SELECTOR = ".lite-information-text__text"
    AUDIT_TRAIL_ID = "audit-trail"
    INPUT_NAME_FILTER_ID = "name"
    CASES_FORM_ID = "form-cases"
    FIRST_LINK_IN_ROW = ".govuk-table__row .govuk-link"
    GOVUK_HEADING = ".govuk-heading-xl"

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BUTTON).click()

    def get_text_of_error_message(self, no):
        return self.driver.find_elements_by_css_selector(self.ERROR_MESSAGE)[no].text

    def get_text_of_body(self):
        return self.driver.find_element_by_css_selector(self.BODY).text

    def get_text_of_caption(self):
        return self.driver.find_element_by_css_selector(self.GOVUK_CAPTION).text

    def get_text_of_table(self):
        return self.driver.find_element_by_css_selector(self.TABLE_CSS).text

    def get_text_of_summary_list(self):
        return self.driver.find_element_by_css_selector(self.SUMMARY_LIST_CSS).text

    def get_text_of_lite_table_body(self):
        return self.driver.find_element_by_css_selector(self.TABLE_BODY_CSS).text

    def get_text_of_cases_form(self):
        return self.driver.find_element_by_id(self.CASES_FORM_ID).text

    def get_text_of_heading(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.GOVUK_HEADING)

    def get_links_in_cells_in_table(self):
        return self.driver.find_elements_by_css_selector(self.LINKS_IN_TABLE)

    def get_number_of_rows_in_lite_table(self):
        return len(self.driver.find_elements_by_css_selector(self.ROWS_IN_CASES_TABLE))

    def get_lite_row_text_by_index(self, index):
        return self.driver.find_elements_by_css_selector(self.ROWS_IN_CASES_TABLE)[int(index)].text

    def get_cells_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_CELL_CSS)

    def get_rows_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_ROW_CSS)

    def get_first_row_of_gov_uk_table(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_ROW_CSS)[0]

    def get_links_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.LINKS_IN_LITE_TABLE)

    def scroll_to_bottom_row(self):
        # Requires that each row have the ID 'row-x' where x is it's index starting from 1
        edit_buttons = self.driver.find_elements_by_css_selector(self.TABLE_ROW_CSS)
        row_index = str(len(edit_buttons))
        scroll_to_element_by_id(self.driver, "row-" + row_index)

    def get_text_of_info_bar(self):
        return self.driver.find_element_by_css_selector(self.SNACKBAR_SELECTOR).text

    def is_flag_applied(self, flag_name: str, parent_selector: str = ""):
        flags = self.driver.find_elements_by_css_selector(parent_selector + ".app-flag")

        for flag in flags:
            if flag_name.lower() in flag.text.lower():
                return True

    def set_header_to_not_stick(self):
        self.driver.execute_script("document.getElementById('app-header').style.position = 'relative';")

    def get_audit_trail_text(self):
        return self.driver.find_element_by_id(self.AUDIT_TRAIL_ID).text

    def go_to_last_page(self):
        self.driver.implicitly_wait(0)
        size = len(self.driver.find_elements_by_css_selector(".lite-pagination__list-item"))
        if size > 0:
            self.driver.find_elements_by_css_selector(".lite-pagination__list-item")[size - 1].click()
        self.driver.implicitly_wait(60)

    def filter_by_name(self, name):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_NAME_FILTER_ID).clear()
        self.driver.find_element_by_id(self.INPUT_NAME_FILTER_ID).send_keys(name)
        functions.click_apply_filters(self.driver)

    def click_first_link_in_row(self):
        self.driver.find_element_by_css_selector(self.FIRST_LINK_IN_ROW).click()

    def try_open_filters(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "lite-filter-bar"))
        )

        if not self.driver.find_element_by_class_name("lite-filter-bar").is_displayed():
            self.driver.find_element_by_id("show-filters-link").click()
            # Delay is necessary as driver can fail to click filters
            time.sleep(0.5)

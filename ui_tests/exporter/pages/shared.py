from ui_tests.exporter.pages.BasePage import BasePage

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Shared(BasePage):
    ORG_NAME_HEADING_ID = "org_name"
    RADIO_BUTTONS = ".govuk-radios__label"  # CSS
    ERROR_MESSAGES = ".govuk-error-summary__body"
    GOV_TABLE_BODY = ".govuk-table__body"
    GOV_TABLE = ".govuk-table"
    GOV_TABLE_ROW = ".govuk-table__row"
    GOV_TABLE_CELL_LINKS = ".govuk-table__cell a"
    GOV_TABLE_CELL = ".govuk-table__cell"
    NOTIFICATION = ".lite-notification-bubble"  # CSS
    MAIN_CONTENT_ID = "main-content"
    FILTERS_LINK_ID = "show-filters-link"
    BUTTON_APPLY_FILTER_ID = "button-apply-filters"
    REFERENCE_ID = "reference"

    def get_text_of_error_messages(self):
        return self.driver.find_element_by_css_selector(self.ERROR_MESSAGES).text

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

    def get_text_of_gov_table(self):
        return self.driver.find_element_by_css_selector(self.GOV_TABLE).text

    def get_table_rows(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_ROW)

    def get_text_of_organisation_heading(self):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, self.ORG_NAME_HEADING_ID))
        )

        return self.driver.find_element_by_id(self.ORG_NAME_HEADING_ID).text

    def get_radio_buttons_elements(self):
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=self.RADIO_BUTTONS)

    def click_on_radio_buttons(self, no):
        radios = self.get_radio_buttons_elements()
        radios[no].click()

    def get_gov_table_cell_links(self):
        return self.driver.find_elements(by=By.CSS_SELECTOR, value=self.GOV_TABLE_CELL_LINKS)

    def get_table_row(self, no):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_ROW)[no]

    def get_links_of_table_row(self, no):
        return self.get_table_row(no).find_elements_by_css_selector(self.GOV_TABLE_CELL_LINKS)

    def get_size_of_table_rows(self):
        return len(self.driver.find_elements_by_css_selector(self.GOV_TABLE_ROW))

    def get_cells_in_gov_table(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_CELL)

    def get_text_of_govuk_table_body(self):
        return self.driver.find_element_by_css_selector(self.GOV_TABLE_BODY).text

    def get_text_of_main_content(self):
        return self.driver.find_element_by_id(self.MAIN_CONTENT_ID).text

    def click_show_filters_link(self):
        self.driver.find_element_by_id(self.FILTERS_LINK_ID).click()

    def filter_by_reference_number(self, reference_number):
        self.click_show_filters_link()
        self.driver.find_element_by_id(self.REFERENCE_ID).send_keys(reference_number)
        self.click_apply_filters_button()

    def click_apply_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTER_ID).click()

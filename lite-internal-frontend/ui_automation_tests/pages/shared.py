from shared.tools.helpers import scroll_to_element_by_id
from shared.BasePage import BasePage


class Shared(BasePage):

    SUBMIT_BUTTON = '.govuk-button[type*="submit"]'  # CSS
    ERROR_MESSAGE = ".govuk-error-message"  # CSS
    LITE_TABLE = ".govuk-table"  # CSS
    LITE_TABLE_BODY = ".govuk-table__body"  # CSS
    LITE_TABLE_ROW = ".govuk-table__body .govuk-table__row"  # CSS
    LITE_TABLE_CELL = ".govuk-table__body .govuk-table__cell"  # CSS
    GOVUK_CAPTION = ".govuk-caption-l"  # CSS
    BODY = "body"  # CSS
    LINKS_IN_TABLE = ".govuk-table td a"
    ROWS_IN_CASES_TABLE = ".govuk-table__body .govuk-table__row"  # CSS
    LINKS_IN_LITE_TABLE = ".govuk-table__cell a"  # CSS
    INFO_BAR = ".lite-info-bar"  # CSS

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT_BUTTON).click()

    def get_text_of_error_message(self, no):
        return self.driver.find_elements_by_css_selector(self.ERROR_MESSAGE)[no].text

    def get_text_of_body(self):
        return self.driver.find_element_by_css_selector(self.BODY).text

    def get_text_of_caption(self):
        return self.driver.find_element_by_css_selector(self.GOVUK_CAPTION).text

    def get_text_of_table(self):
        return self.driver.find_element_by_css_selector(self.LITE_TABLE).text

    def get_text_of_lite_table_body(self):
        return self.driver.find_element_by_css_selector(self.LITE_TABLE_BODY).text

    def get_links_in_cells_in_table(self):
        return self.driver.find_elements_by_css_selector(self.LINKS_IN_TABLE)

    def get_number_of_rows_in_lite_table(self):
        return len(self.driver.find_elements_by_css_selector(self.ROWS_IN_CASES_TABLE))

    def get_lite_row_text_by_index(self, index):
        return self.driver.find_elements_by_css_selector(self.ROWS_IN_CASES_TABLE)[int(index)].text

    def get_cells_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.LITE_TABLE_CELL)

    def get_rows_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.LITE_TABLE_ROW)

    def get_first_row_of_gov_uk_table(self):
        return self.driver.find_elements_by_css_selector(self.LITE_TABLE_ROW)[0]

    def get_links_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.LINKS_IN_LITE_TABLE)

    def scroll_to_bottom_row(self):
        # Requires that each row have the ID 'row-x' where x is it's index starting from 1
        edit_buttons = self.driver.find_elements_by_css_selector(self.LITE_TABLE_ROW)
        row_index = str(len(edit_buttons))
        scroll_to_element_by_id(self.driver, "row-" + row_index)

    def get_text_of_info_bar(self):
        return self.driver.find_element_by_css_selector(self.INFO_BAR).text

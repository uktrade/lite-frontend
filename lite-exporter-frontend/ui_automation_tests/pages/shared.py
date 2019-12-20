from shared.BasePage import BasePage


class Shared(BasePage):
    HEADING = ".govuk-heading-xl"  # CSS
    RADIO_BUTTONS = ".govuk-radios__label"  # CSS
    ERROR_MESSAGES = ".govuk-error-summary__body"
    ERROR_MESSAGE = ".govuk-error-message"
    GOV_TABLE_BODY = ".govuk-table__body"
    GOV_GRID_ROW = ".govuk-grid-row"
    GOV_TABLE = ".govuk-table"
    GOV_TABLE_ROW = ".govuk-table__row"
    GOV_TABLE_CELL_LINKS = ".govuk-table__cell a"
    GOV_TABLE_CELL = ".govuk-table__cell"
    H2 = "h2"
    H1 = "h1"
    LITE_SECTION = ".lite-section"
    NOTIFICATION = ".lite-notification-bubble"  # CSS

    def get_text_of_error_messages(self):
        return self.driver.find_element_by_css_selector(self.ERROR_MESSAGES).text

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(self.ERROR_MESSAGES).is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

    def get_text_of_gov_table(self):
        return self.driver.find_element_by_css_selector(self.GOV_TABLE).text

    def get_table_rows(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_ROW)

    def get_text_of_heading(self):
        return self.driver.find_element_by_css_selector(self.HEADING).text

    def get_radio_buttons_elements(self):
        return self.driver.find_elements_by_css_selector(self.RADIO_BUTTONS)

    def click_on_radio_buttons(self, no):
        return self.driver.find_elements_by_css_selector(self.RADIO_BUTTONS)[no].click()

    def get_text_of_gov_grid_row(self):
        return self.driver.find_element_by_css_selector(self.GOV_GRID_ROW).text

    def get_gov_table_cell_links(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_CELL_LINKS)

    def get_table_row(self, no):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_ROW)[no]

    def get_links_of_table_row(self, no):
        return self.get_table_row(no).find_elements_by_css_selector(self.GOV_TABLE_CELL_LINKS)

    def get_text_of_h2(self):
        return self.driver.find_element_by_tag_name(self.H2).text

    def get_text_of_h1(self):
        return self.driver.find_element_by_tag_name(self.H1).text

    def get_size_of_table_rows(self):
        return len(self.driver.find_elements_by_css_selector(self.GOV_TABLE_ROW))

    def get_cells_in_gov_table(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLE_CELL)

    def get_text_of_govuk_table_body(self):
        return self.driver.find_element_by_css_selector(self.GOV_TABLE_BODY).text

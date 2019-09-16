from helpers.BasePage import BasePage


class Shared(BasePage):

    submit_button = '.govuk-button[type*="submit"]'  # CSS
    error_message = '.govuk-error-message'  # CSS
    lite_table = '.lite-table'  # CSS
    lite_table_body = '.lite-table__body'  # CSS
    lite_table_row = '.lite-table__body .lite-table__row'  # CSS
    lite_table_cell = '.lite-table__body .lite-table__cell'  # CSS
    lite_table_cell_no_body = '.lite-table__cell'  # CSS
    govuk_table_body = '.govuk-table__body'  # CSS
    govuk_caption = '.govuk-caption-l'  # CSS
    selected_tab = '.lite-tabs__tab.selected'  # CSS
    body = 'body'  # CSS
    links_in_table = '.lite-table td a'
    rows_in_cases_table = '.lite-cases-table .lite-cases-table-row'  # CSS
    h1 = 'h1'  # CSS
    links_in_lite_table = '.lite-table__cell a'  # CSS
    govuk_panel_body = '.govuk-panel__body'  # CSS
    back_link = '.govuk-back-link'  # CSS
    info_bar = '.lite-info-bar'  # CSS

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_back(self):
        self.driver.find_element_by_css_selector(self.back_link).click()

    def get_text_of_error_message(self, no):
        return self.driver.find_elements_by_css_selector(self.error_message)[no].text

    def get_text_of_body(self):
        return self.driver.find_element_by_css_selector(self.body).text

    def get_text_of_selected_tab(self):
        return self.driver.find_element_by_css_selector(self.selected_tab).text

    def get_text_of_table_body(self):
        return self.driver.find_element_by_css_selector(self.govuk_table_body).text

    def get_text_of_panel_body(self):
        return self.driver.find_element_by_css_selector(self.govuk_panel_body).text

    def get_text_of_caption(self):
        return self.driver.find_element_by_css_selector(self.govuk_caption).text

    def get_text_of_table(self):
        return self.driver.find_element_by_css_selector(self.lite_table).text

    def get_text_of_lite_table_body(self):
        return self.driver.find_element_by_css_selector(self.lite_table_body).text

    def get_text_of_h1(self):
        return self.driver.find_element_by_css_selector(self.h1).text

    def get_links_in_cells_in_table(self):
        return self.driver.find_elements_by_css_selector(self.links_in_table)

    def get_number_of_rows_in_lite_table(self):
        return len(self.driver.find_elements_by_css_selector(self.rows_in_cases_table))

    def get_lite_row_text_by_index(self, index):
        return self.driver.find_elements_by_css_selector(self.rows_in_cases_table)[int(index)].text

    def get_cells_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.lite_table_cell)

    def get_cells_in_lite_table_no_body(self):
        return self.driver.find_elements_by_css_selector(self.lite_table_cell_no_body)

    def get_rows_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.lite_table_row)

    def get_links_in_lite_table(self):
        return self.driver.find_elements_by_css_selector(self.links_in_lite_table)

    def get_text_of_info_bar(self):
        return self.driver.find_element_by_css_selector(self.info_bar).text

    def click_back_link(self):
        return self.driver.find_element_by_css_selector(self.back_link).click()


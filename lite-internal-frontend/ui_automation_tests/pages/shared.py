from helpers.BasePage import BasePage


class Shared(BasePage):

    submit_button = '[type*="submit"]'  # CSS
    error_message = '.govuk-error-message'  # CSS
    lite_table = '.lite-table'  # CSS
    lite_table_body = '.lite-table__body'  # CSS
    govuk_table_body = '.govuk-table__body'  # CSS
    govuk_caption = '.govuk-caption-l'  # CSS
    selected_tab = '.lite-tabs__tab.selected'  # CSS
    body = 'body'  # CSS
    links_in_table = ".lite-table td a"

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def get_text_of_error_message(self, no):
        return self.driver.find_elements_by_css_selector(self.error_message)[no].text

    def get_text_of_body(self):
        return self.driver.find_element_by_css_selector(self.body).text

    def get_text_of_selected_tab(self):
        return self.driver.find_element_by_css_selector(self.selected_tab).text

    def get_text_of_table_body(self):
        return self.driver.find_element_by_css_selector(self.govuk_table_body).text

    def get_text_of_caption(self):
        return self.driver.find_element_by_css_selector(self.govuk_caption).text

    def get_text_of_table(self):
        return self.driver.find_element_by_css_selector(self.lite_table).text

    def get_text_of_lite_table_body(self):
        return self.driver.find_element_by_css_selector(self.lite_table_body).text

    def get_links_in_cells_in_table(self):
        return self.driver.find_elements_by_css_selector(self.links_in_table)

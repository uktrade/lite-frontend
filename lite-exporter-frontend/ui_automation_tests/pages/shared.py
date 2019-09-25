class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.heading = ".govuk-heading-xl"  # CSS
        self.radio_buttons = ".govuk-radios__label"  # CSS
        self.submit_button = "button[type*='submit']"
        self.back_link = ".govuk-back-link"
        self.error_messages = ".govuk-error-summary__body"
        self.error_message = ".govuk-error-message"
        self.gov_body = ".govuk-body"
        self.gov_grid_row = ".govuk-grid-row"
        self.gov_table = ".govuk-table"
        self.gov_table_row = ".govuk-table__row"
        self.gov_table_cell_links = ".govuk-table__cell a"
        self.application_name = "a[href*='overview']"
        self.h2 = "h2"
        self.h1 = "h1"
        self.lite_section = ".lite-section"
        self.notification = ".app-icon-label__notification"  # CSS

    def get_text_of_error_messages(self):
        return self.driver.find_element_by_css_selector(self.error_messages).text

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_back_link(self):
        self.driver.find_element_by_css_selector(self.back_link).click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(self.error_messages).is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

    def get_text_of_gov_table(self):
        return self.driver.find_element_by_css_selector(self.gov_table).text

    def get_table_rows(self):
        return self.driver.find_elements_by_css_selector(self.gov_table_row)

    def get_text_of_heading(self):
        return self.driver.find_element_by_css_selector(self.heading).text

    def get_radio_buttons_elements(self):
        return self.driver.find_elements_by_css_selector(self.radio_buttons)

    def click_on_radio_buttons(self, no):
        return self.driver.find_elements_by_css_selector(self.radio_buttons)[no].click()

    def get_text_of_gov_body(self):
        return self.driver.find_element_by_css_selector(self.gov_body).text

    def get_text_of_gov_grid_row(self):
        return self.driver.find_element_by_css_selector(self.gov_grid_row).text

    def get_gov_table_cell_links(self):
        return self.driver.find_elements_by_css_selector(self.gov_table_cell_links)

    def get_table_row(self, no):
        return self.driver.find_elements_by_css_selector(self.gov_table_row)[no]

    def get_links_of_table_row(self, no):
        return self.get_table_row(no).find_elements_by_css_selector(self.gov_table_cell_links)

    def get_text_of_h2(self):
        return self.driver.find_element_by_tag_name(self.h2).text

    def get_text_of_h1(self):
        return self.driver.find_element_by_tag_name(self.h1).text

    def get_lite_sections(self):
        return self.driver.find_elements_by_css_selector(self.lite_section)

    def get_size_of_table_rows(self):
        return len(self.driver.find_elements_by_css_selector(self.gov_table_row))

    def click_on_application_name(self):
        return self.driver.find_element_by_css_selector(self.application_name).click()


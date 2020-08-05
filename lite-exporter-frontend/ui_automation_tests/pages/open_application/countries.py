from ui_automation_tests.pages.BasePage import BasePage


class OpenApplicationCountriesPage(BasePage):

    CHECKBOX_COUNTRIES_SELECTOR = ".govuk-checkboxes__input"
    COUNTRIES_LABELS = ".govuk-checkboxes__label"
    COUNTRIES_SEARCH_BOX = "filter-box"  # ID
    COUNTRIES_LIST_SELECTOR = ".govuk-checkboxes"
    LINK_SELECT_ALL_ID = "link-select-all"

    STATIC_DESTINATIONS_LIST_SELECTOR = ".govuk-list"

    def get_countries_names(self):
        countries_names = []
        for country in self.driver.find_elements_by_css_selector(self.COUNTRIES_LABELS):
            countries_names.append(country.text)
        return countries_names

    def select_country(self, name):
        checkbox = self.driver.find_element_by_id(name)
        checkbox.click()

    def search_for_country(self, country):
        self.driver.find_element_by_id(self.COUNTRIES_SEARCH_BOX).send_keys(country)

    def get_text_of_countries_list(self):
        return self.driver.find_elements_by_css_selector(self.COUNTRIES_LIST_SELECTOR)[0].text

    def click_select_all(self):
        self.driver.find_element_by_id(self.LINK_SELECT_ALL_ID).click()

    def get_number_of_checkboxes(self, checked=False):
        if checked:
            return len(self.driver.find_elements_by_css_selector("input[type='checkbox']:checked"))
        else:
            return len(self.driver.find_elements_by_css_selector(self.CHECKBOX_COUNTRIES_SELECTOR))

    def get_static_destinations_list(self):
        countries_names = []
        country_list_element = self.driver.find_element_by_css_selector(self.STATIC_DESTINATIONS_LIST_SELECTOR)
        for country in country_list_element.find_elements_by_tag_name("li"):
            countries_names.append(country.text)
        return countries_names

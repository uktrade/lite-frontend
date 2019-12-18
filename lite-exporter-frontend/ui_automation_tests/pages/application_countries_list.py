from shared.BasePage import BasePage


class ApplicationCountriesList(BasePage):
    COUNTRIES_CHECKBOX = ".govuk-checkboxes__input"
    COUNTRIES_LABELS = ".govuk-checkboxes__label"
    COUNTRIES_SEARCH_BOX = "filter-box"  # ID
    COUNTRIES_LIST_SELECTOR = "#pane_countries .govuk-checkboxes"
    SELECT_ALL_LINK = "link-select-all"  # ID

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
        self.driver.find_element_by_id(self.SELECT_ALL_LINK).click()

    def get_number_of_checkboxes(self, checked=False):
        if checked:
            return len(self.driver.find_elements_by_css_selector("input[type='checkbox']:checked"))
        else:
            return len(self.driver.find_elements_by_css_selector(self.COUNTRIES_CHECKBOX))

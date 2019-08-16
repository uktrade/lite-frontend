class ApplicationCountriesList:

    def __init__(self, driver):
        self.driver = driver
        self.countries_checkboxes = ".govuk-checkboxes__input"
        self.countries_labels = ".govuk-checkboxes__label"
        self.countries_search_box = "filter-box"   # ID
        self.countries_list = "pane_countries"   # ID

    def get_countries_names(self):
        countries_names = []
        for country in self.driver.find_elements_by_css_selector(self.countries_labels):
            countries_names.append(country.text)
        return countries_names

    def view_countries(self):
        for checkbox in self.driver.find_elements_by_css_selector(self.countries_checkboxes):
            checkbox.click()

    def select_country(self, name):
        checkbox = self.driver.find_element_by_id(name)
        checkbox.click()

    def search_for_country(self, country):
        self.driver.find_element_by_id(self.countries_search_box).send_keys(country)

    def get_text_of_countries_list(self):
        return self.driver.find_element_by_id(self.countries_list).text

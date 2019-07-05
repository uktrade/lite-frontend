class ApplicationOverviewPage:

    def __init__(self, driver):
        self.driver = driver
        self.location_link = "location"
        self.countries_link = "countries"
        self.goods_link = "goods"
        self.end_user_link = "end_users"
        self.sites_link = "a[href*='sites']"
        self.goods_link = "goods"
        self.show_countries_link = "[onclick*='showCountries']"
        self.modal_close = "modal-close-button" #id
        self.modal_content = ".modal-content" #css
        self.gov_tables = ".govuk-table__body" #css

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.location_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.location_link).click()

    def click_goods_link(self):
        element = self.driver.find_element_by_id(self.goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def click_end_user_link(self):
        element = self.driver.find_element_by_id(self.end_user_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.countries_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.countries_link).click()

    def get_text_of_countries_selected(self):
        return self.driver.find_element_by_css_selector(self.show_countries_link).text

    def click_on_countries_selected(self):
        self.driver.find_element_by_css_selector(self.show_countries_link).click()

    def click_on_modal_close(self):
        self.driver.find_element_by_id(self.modal_close).click()

    def get_text_of_country_modal_content(self):
        return self.driver.find_element_by_css_selector(self.modal_content).text

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.gov_tables)[len(self.driver.find_elements_by_css_selector(self.gov_tables))-1].text

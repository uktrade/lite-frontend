class GoodsCountriesPage:
    def __init__(self, driver):
        self.driver = driver
        self.gov_checkboxes_input = ".govuk-checkboxes__input"  # css selector
        self.select_all_id = "link-select-all"  # id
        self.deselect_all_id = "link-deselect-all"  # id

    def select_all(self):
        elements = self.driver.find_elements_by_css_selector(self.gov_checkboxes_input)
        for element in elements:
            if not element.is_selected():
                element.click()

    def select_all_link(self):
        self.driver.find_element_by_id(self.select_all_id).click()

    def deselect_all(self):
        elements = self.driver.find_elements_by_css_selector(self.gov_checkboxes_input)
        for element in elements:
            if element.is_selected():
                element.click()

    def deselect_all_link(self):
        self.driver.find_element_by_id(self.deselect_all_id).click()

    def all_selected(self):
        elements = self.driver.find_elements_by_css_selector(self.gov_checkboxes_input)
        for element in elements:
            if not element.is_selected():
                return False

        return True

    def all_deselected(self):
        elements = self.driver.find_elements_by_css_selector(self.gov_checkboxes_input)
        for element in elements:
            if element.is_selected():
                return False

        return True

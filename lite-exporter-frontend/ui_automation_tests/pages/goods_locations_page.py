class GoodsLocationsPage:
    def __init__(self, driver):
        self.driver = driver
        self.edit_sites_button = 'a[href*="existing-sites"]'

    def click_edit_sites_button(self):
        self.driver.find_element_by_css_selector(self.edit_sites_button).click()

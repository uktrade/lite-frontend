class DepartmentOfInternationalTradeHub():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.manage_cases_btn = "a[href*='/cases']"
        self.manage_organisations_link = "a[href*='/organisations']"

    def go_to(self, url):
        self.driver.get(url)

    def click_manage_cases_btn(self):
        self.driver.find_element_by_css_selector(self.manage_cases_btn).click()

    def click_manage_organisations_link(self):
        self.driver.find_element_by_id("lite-menu-button").click()
        self.driver.find_element_by_css_selector(self.manage_organisations_link).click()

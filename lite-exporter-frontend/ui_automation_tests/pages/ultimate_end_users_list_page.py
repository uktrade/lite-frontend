class UltimateEndUsersListPage:

    def __init__(self, driver):
        self.driver = driver
        self.govuk_button = ".govuk-button"

    def click_on_add_ultimate_end_user(self):
        self.driver.find_element_by_css_selector(self.govuk_button).click()

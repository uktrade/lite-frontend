from shared.BasePage import BasePage


class ExternalLocationsPage(BasePage):

    ADD_NEW_ADDRESS_BUTTON = "//a[contains(@href, 'add')]"
    PREEXISTING_LOCATIONS_BUTTON = "a[href*=preexisting"

    def click_add_new_address(self):
        self.driver.find_element_by_xpath(self.ADD_NEW_ADDRESS_BUTTON).click()

    def click_preexisting_locations(self):
        self.driver.find_element_by_css_selector(self.PREEXISTING_LOCATIONS_BUTTON).click()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.functions import element_with_css_selector_exists


class OpenLicenceReturnsPage(BasePage):
    SUBMIT_RETURN_BUTTON_ID = "submit-return"
    YEAR_SELECT_ID = "year"
    SUCCESS_PANEL_CSS_SELECTOR = ".govuk-panel--confirmation"

    def click_submit_return(self):
        self.driver.find_element(by=By.ID, value=self.SUBMIT_RETURN_BUTTON_ID).click()

    def select_year(self, year):
        Select(self.driver.find_element(by=By.ID, value=self.YEAR_SELECT_ID)).select_by_value(str(year))

    def success_panel_is_present(self):
        return element_with_css_selector_exists(self.driver, self.SUCCESS_PANEL_CSS_SELECTOR)

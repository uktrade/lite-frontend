from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class GoodsCountriesPage(BasePage):

    GOV_CHECKBOXES_INPUT = ".govuk-checkboxes__input"  # css selector
    SELECT_ALL_ID = "link-select-all"  # id
    DESELECT_ALL_ID = "link-deselect-all"  # id
    SAVE_BUTTON = "button[type='submit']"

    def select_all_link(self):
        self.driver.find_element(by=By.ID, value=self.SELECT_ALL_ID).click()

    def deselect_all_link(self):
        self.driver.find_element(by=By.ID, value=self.DESELECT_ALL_ID).click()

    def all_selected(self):
        elements = self.driver.find_elements_by_css_selector(self.GOV_CHECKBOXES_INPUT)
        for element in elements:
            if not element.is_selected():
                return False

        return True

    def all_deselected(self):
        elements = self.driver.find_elements_by_css_selector(self.GOV_CHECKBOXES_INPUT)
        for element in elements:
            if element.is_selected():
                return False

        return True

    def click_save(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.SAVE_BUTTON).click()

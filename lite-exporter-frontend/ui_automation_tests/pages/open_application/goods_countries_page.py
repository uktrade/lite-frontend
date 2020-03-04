from ui_automation_tests.shared.BasePage import BasePage


class GoodsCountriesPage(BasePage):

    GOV_CHECKBOXES_INPUT = ".govuk-checkboxes__input"  # css selector
    SELECT_ALL_ID = "link-select-all"  # id
    DESELECT_ALL_ID = "link-deselect-all"  # id
    SAVE_BUTTON = "button[type='submit']"

    def select_all_link(self):
        self.driver.find_element_by_id(self.SELECT_ALL_ID).click()

    def deselect_all_link(self):
        self.driver.find_element_by_id(self.DESELECT_ALL_ID).click()

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
        self.driver.find_element_by_css_selector(self.SAVE_BUTTON).click()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.exporter.pages.BasePage import BasePage


class StandardApplicationGoodDetails(BasePage):

    INPUT_VALUE_ID = "value"
    INPUT_QUANTITY_ID = "quantity"
    SELECT_UNIT_ID = "unit"
    RADIO_INCORPORATED = "is_good_incorporated"
    RADIO_DEACTIVATED = "is_deactivated"
    RADIO_PROOF_MARKS = "has_proof_mark"

    def enter_value(self, value):
        self.driver.find_element(
            by=By.XPATH, value=f"//input[@type='text' and contains(@id, '{self.INPUT_VALUE_ID}')]"
        ).send_keys(value)

    def enter_quantity(self, quantity):
        self.driver.find_element_by_id(self.INPUT_QUANTITY_ID).send_keys(quantity)

    def select_unit(self, unit):
        Select(self.driver.find_element_by_id(self.SELECT_UNIT_ID)).select_by_visible_text(unit)

    def set_good_incorporated(self, value):
        self._set_radio(self.RADIO_INCORPORATED, value)

    def set_deactivated_status(self, value):
        suffix = {True: "0", False: "1"}[value]
        self._set_radio(f"{self.RADIO_DEACTIVATED}_{suffix}", value)

    def set_proof_marks(self, value):
        self._set_radio(self.RADIO_PROOF_MARKS, value)

    def _set_radio(self, identifier, value):
        self.driver.find_element(
            by=By.XPATH, value=f"//input[@type='radio' and contains(@id, '{identifier}') and @value='{value}']"
        ).click()

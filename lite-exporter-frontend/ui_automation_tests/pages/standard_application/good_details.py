from selenium.webdriver.support.select import Select

from ui_automation_tests.shared.BasePage import BasePage


class StandardApplicationGoodDetails(BasePage):

    INPUT_VALUE_ID = "value"
    INPUT_QUANTITY_ID = "quantity"
    SELECT_UNIT_ID = "unit"
    RADIO_IS_GOOD_INCORPORATED_TRUE_ID = "is_good_incorporated-True"
    RADIO_IS_GOOD_INCORPORATED_FALSE_ID = "is_good_incorporated-False"

    def enter_value(self, value):
        self.driver.find_element_by_id(self.INPUT_VALUE_ID).send_keys(value)

    def enter_quantity(self, quantity):
        self.driver.find_element_by_id(self.INPUT_QUANTITY_ID).send_keys(quantity)

    def select_unit(self, unit):
        Select(self.driver.find_element_by_id(self.SELECT_UNIT_ID)).select_by_visible_text(unit)

    def check_is_good_incorporated_true(self):
        self.driver.find_element_by_id(self.RADIO_IS_GOOD_INCORPORATED_TRUE_ID).click()

    def check_is_good_incorporated_false(self):
        self.driver.find_element_by_id(self.RADIO_IS_GOOD_INCORPORATED_FALSE_ID).click()

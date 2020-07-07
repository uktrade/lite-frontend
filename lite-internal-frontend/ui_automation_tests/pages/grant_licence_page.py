from pages.BasePage import BasePage


class GrantLicencePage(BasePage):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"
    DURATION_TEXT = "duration"
    GOOD_QUANTITY_PARTIAL_ID = "quantity-"
    GOOD_VALUE_PARTIAL_ID = "value-"

    def get_duration_in_finalise_view(self):
        return self.driver.find_element_by_id(self.DURATION_TEXT).get_attribute("value")

    def get_date_in_date_entry(self):
        return {
            "day": self.driver.find_element_by_id(self.DAY).get_attribute("value"),
            "month": self.driver.find_element_by_id(self.MONTH).get_attribute("value"),
            "year": self.driver.find_element_by_id(self.YEAR).get_attribute("value"),
        }

    def get_good_quantity(self, id):
        return self.driver.find_element_by_id(self.GOOD_QUANTITY_PARTIAL_ID + id).get_attribute("value")

    def get_good_value(self, id):
        return self.driver.find_element_by_id(self.GOOD_VALUE_PARTIAL_ID + id).get_attribute("value")

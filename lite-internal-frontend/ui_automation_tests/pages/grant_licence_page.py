from pages.BasePage import BasePage


class GrantLicencePage(BasePage):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"
    DURATION_TEXT = "duration"
    GOOD_QUANTITY_PARTIAL_ID = "quantity-"
    GOOD_VALUE_PARTIAL_ID = "value-"
    GOOD_USAGE_QUANTITY_PARTIAL_ID = "quantity-usage-"
    GOOD_USAGE_VALUE_PARTIAL_ID = "value-usage-"
    GOOD_APPLIED_FOR_QUANTITY_PARTIAL_ID = "quantity-applied-for-"
    GOOD_APPLIED_FOR_VALUE_PARTIAL_ID = "value-applied-for-"

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

    def get_good_usage_quantity(self, id):
        return self.driver.find_element_by_id(self.GOOD_USAGE_QUANTITY_PARTIAL_ID + id).text

    def get_good_usage_value(self, id):
        return self.driver.find_element_by_id(self.GOOD_USAGE_VALUE_PARTIAL_ID + id).text

    def get_good_applied_for_quantity(self, id):
        return self.driver.find_element_by_id(self.GOOD_APPLIED_FOR_QUANTITY_PARTIAL_ID + id).text

    def get_good_applied_for_value(self, id):
        return self.driver.find_element_by_id(self.GOOD_APPLIED_FOR_VALUE_PARTIAL_ID + id).text

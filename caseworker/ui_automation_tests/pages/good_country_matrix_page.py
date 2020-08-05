from ui_automation_tests.pages.BasePage import BasePage


class GoodCountryMatrixPage(BasePage):
    ENABLED_GOOD_COUNTRY_DECISION_ROW_PARTIAL_ID = "decision-"
    REFUSED_GOOD_COUNTRY_DECISION_ROW_PARTIAL_ID = "refused-"

    def get_enabled_good_country_decision_row(self, goods_type_id):
        return self.driver.find_element_by_id(self.ENABLED_GOOD_COUNTRY_DECISION_ROW_PARTIAL_ID + goods_type_id).text

    def get_refused_good_country_decision_row(self, goods_type_id):
        return self.driver.find_element_by_id(self.REFUSED_GOOD_COUNTRY_DECISION_ROW_PARTIAL_ID + goods_type_id).text

    def select_good_country_option(self, decision, goods_type_id, country_id):
        self.driver.find_element_by_id(f"{decision}-{goods_type_id}.{country_id}").click()

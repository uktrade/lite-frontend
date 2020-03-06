from ui_automation_tests.shared.BasePage import BasePage


class ExhibitionClearanceGoodPage(BasePage):
    GOOD_TYPE_PARTIAL_ID = "item_type-"

    def click_good_type(self, type):
        self.driver.find_element_by_id(self.GOOD_TYPE_PARTIAL_ID + type).click()

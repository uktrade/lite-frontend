from helpers.BasePage import BasePage


class GoodSummaryPage(BasePage):
    EDIT_GOODS_FLAGS = "button-edit-goods-flags"  # ID
    ADD_REPORT_SUMMARY = "button-add-report-summary"  # ID

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.EDIT_GOODS_FLAGS)
        edit_goods_btn.click()

    def click_add_report_summary(self):
        self.driver.find_element_by_id(self.ADD_REPORT_SUMMARY).click()

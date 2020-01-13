from pages.shared import Shared
from shared.BasePage import BasePage


class GoodsListPage(BasePage):

    BUTTON_ADD_A_GOOD_ID = "button-add-a-good"

    def assert_goods_are_displayed_of_good_name(self, driver, description, part_number, control_code):
        goods_row = Shared(driver).get_text_of_gov_table()

        assert description in goods_row
        assert part_number in goods_row
        assert control_code in goods_row

    def assert_clc_goods_are_displayed_of_good_name(self, driver, description, part_number, control_code):
        goods_row = Shared(driver).get_text_of_gov_table()

        assert description in goods_row
        assert part_number in goods_row
        assert control_code in goods_row
        assert "Control List Classification Query" in goods_row

    def select_a_draft_good(self):
        draft_goods = "//*[contains(text(), 'Draft')]//..//a"
        self.driver.find_elements_by_xpath(draft_goods)[0].click()

    def click_add_a_good(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_GOOD_ID).click()

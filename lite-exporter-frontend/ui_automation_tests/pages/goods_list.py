from shared.BasePage import BasePage


class GoodsListPage(BasePage):

    BUTTON_ADD_A_GOOD_ID = "button-add-a-good"

    def select_a_draft_good(self):
        draft_goods = "//*[contains(text(), 'Draft')]//..//a"
        self.driver.find_elements_by_xpath(draft_goods)[0].click()

    def click_add_a_good(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_GOOD_ID).click()

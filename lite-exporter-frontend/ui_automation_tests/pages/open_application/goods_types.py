from selenium.common.exceptions import NoSuchElementException

from ui_automation_tests.shared.BasePage import BasePage


class OpenApplicationGoodsTypesPage(BasePage):

    BUTTON_ADD_GOOD_ID = "button-add-good"
    GOODS_TYPE_INFO = ".govuk-table__row"
    REMOVE_GOODS_TYPE_LINK = "a[href*='goods-types']"

    def click_add_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_GOOD_ID).click()

    def get_text_of_goods_type_info(self, num):
        return self.driver.find_elements_by_css_selector(self.GOODS_TYPE_INFO)[num].text

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_GOODS_TYPE_LINK)
        except NoSuchElementException:
            return None

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class OpenApplicationGoodsTypesPage(BasePage):

    BUTTON_ADD_GOOD_ID = "button-add-good"
    GOODS_TYPE_INFO = ".govuk-table__row"
    REMOVE_GOODS_TYPE_LINK = "a[href*='goods-types']"

    def click_add_good_button(self):
        self.driver.find_element(by=By.ID, value=self.BUTTON_ADD_GOOD_ID).click()

    def get_text_of_goods_type_info(self, num):
        return self.driver.find_elements_by_css_selector(self.GOODS_TYPE_INFO)[num].text

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element(by=By.CSS_SELECTOR, value=self.REMOVE_GOODS_TYPE_LINK)
        except NoSuchElementException:
            return None

    def get_number_of_goods(self):
        return self.driver.find_elements_by_css_selector(self.GOODS_TYPE_INFO)

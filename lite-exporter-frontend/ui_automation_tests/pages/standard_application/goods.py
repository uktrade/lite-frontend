from selenium.common.exceptions import NoSuchElementException
from ui_automation_tests.shared.BasePage import BasePage

from ui_automation_tests.shared import functions


class StandardApplicationGoodsPage(BasePage):

    BUTTON_ADD_NEW_GOOD_ID = "button-add-new-good"
    BUTTON_ADD_PREEXISTING_GOOD_ID = "button-add-preexisting-good"
    SPAN_GOODS_TOTAL_VALUE = "span-goods-total-value"
    GOOD_ENTRY = ".govuk-table__body .govuk-table__row"
    TABLE_BODY = "tbody"
    TABLE_ROW = "tr"
    ADD_TO_APPLICATION_ID = "add-to-application"
    REMOVE_GOOD_LINK = "a[href*='good-on-application']"
    REMOVE_GOODS_TYPE_LINK = "a[href*='goods-types/remove']"

    def click_add_new_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_NEW_GOOD_ID).click()

    def click_add_preexisting_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_PREEXISTING_GOOD_ID).click()

    def get_goods(self):
        return self.driver.find_elements_by_css_selector(self.TABLE_BODY + " " + self.TABLE_ROW)

    def get_goods_total_value(self):
        return self.driver.find_element_by_id(self.SPAN_GOODS_TOTAL_VALUE).text

    def get_goods_count(self):
        return len(self.driver.find_elements_by_css_selector(self.GOOD_ENTRY))

    def click_add_to_application(self):
        # Click the "Add to application" link on the first good
        self.driver.find_element_by_id(self.ADD_TO_APPLICATION_ID).click()

    def get_remove_good_link(self):
        return self.driver.find_element_by_css_selector(self.REMOVE_GOOD_LINK)

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_GOODS_TYPE_LINK)
        except NoSuchElementException:
            return None

    def goods_exist_on_the_application(self):
        return functions.element_with_css_selector_exists(self.driver, self.REMOVE_GOOD_LINK)

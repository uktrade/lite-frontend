from selenium.common.exceptions import NoSuchElementException


class ApplicationGoodsTypeList:

    def __init__(self, driver):
        self.driver = driver
        self.add_goods_type_button = ".govuk-button"
        self.goods_type_info = ".govuk-table__row"
        self.goods_type_table_overview = "good_types_table_overview"   # ID
        self.remove_goods_type_link = "a[href*='goods-types']"

    def click_goods_type_button(self):
        self.driver.find_element_by_css_selector(self.add_goods_type_button).click()

    def get_text_of_goods_type_info(self, num):
        return self.driver.find_elements_by_css_selector(self.goods_type_info)[num].text

    def get_text_of_goods_type_info_overview(self):
        return self.driver.find_element_by_id(self.goods_type_table_overview).text

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.remove_goods_type_link)
        except NoSuchElementException:
            return None

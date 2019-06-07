class GoodsList():

    def __init__(self, driver):
        self.driver = driver
        self.goods_edit_link = "[href*='goods/edit']"
        self.goods_delete_link = "[href*='goods/delete']"
        self.goods_delete_button = ".govuk-button--warning"


    def assert_goods_are_displayed_of_good_name(self, description, part_number, control_code):
        goods_row = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + description + "')]]")
        assert goods_row.is_displayed()
        assert goods_row.find_element_by_xpath(".//following-sibling::td").text == part_number
        assert goods_row.find_element_by_xpath(".//following-sibling::td[2]").text == control_code

    def click_on_goods_edit_link(self, number):
        self.driver.find_elements_by_css_selector(self.goods_edit_link)[number].click()

    def click_on_goods_delete_link(self, number):
        self.driver.find_elements_by_css_selector(self.goods_delete_link)[number].click()

    def click_on_delete_good_button(self):
        self.driver.find_element_by_css_selector(self.goods_delete_button).click()

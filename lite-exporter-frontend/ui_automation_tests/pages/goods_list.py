class GoodsList():

    def __init__(self, driver):
        self.driver = driver
        self.goods_edit_link = "[href*='goods/edit']"
        self.goods_delete_link = "[href*='goods/delete']"
        self.goods_delete_button = ".govuk-button--warning"
        self.description_xpath_prefix = "//*[text()[contains(.,'%s')]]"
        self.part_number_xpath_prefix = "%s/../*[text()[contains(.,'%s')]]"
        self.control_code_xpath_prefix = "%s/../*[text()[contains(.,'%s')]]"

    def assert_goods_are_displayed_of_good_name(self, description, part_number, control_code):
        description_xpath = self.description_xpath_prefix % description
        part_number_xpath = self.part_number_xpath_prefix % (description_xpath, part_number)
        control_code_xpath = self.control_code_xpath_prefix % (description_xpath, control_code)

        goods_row = self.driver.find_element_by_xpath(description_xpath)
        goods_row_part_number = self.driver.find_element_by_xpath(part_number_xpath)
        goods_row_control_code = self.driver.find_element_by_xpath(control_code_xpath)

        assert goods_row.is_displayed()
        assert goods_row_part_number.is_displayed()
        assert goods_row_control_code.is_displayed()

    def click_on_goods_edit_link(self, number):
        self.driver.find_elements_by_css_selector(self.goods_edit_link)[number].click()

    def click_on_goods_delete_link(self, number):
        self.driver.find_elements_by_css_selector(self.goods_delete_link)[number].click()

    def click_on_delete_good_button(self):
        self.driver.find_element_by_css_selector(self.goods_delete_button).click()

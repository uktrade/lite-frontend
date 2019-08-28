from pages.shared import Shared


class GoodsList:

    # Selector for the edit/delete goods link in the table
    EDIT_LINK = '[href*="goods/edit"]'
    DELETE_LINK = '[href*="goods/delete"]'

    # This is for the delete confirmation page
    DELETE_BUTTON = '.govuk-button--warning'

    def __init__(self, driver):
        self.driver = driver

    def assert_goods_are_displayed_of_good_name(self, driver, description, part_number, control_code):
        goods_row = Shared(driver).get_text_of_gov_table()

        assert description in goods_row
        assert part_number in goods_row
        assert control_code in goods_row

    def assert_clc_goods_are_displayed_of_good_name (self, driver, description, part_number, control_code):
        goods_row = Shared(driver).get_text_of_gov_table()

        assert description in goods_row
        assert part_number in goods_row
        assert control_code in goods_row
        assert 'N/A: In CLC query' in goods_row

    def click_on_goods_edit_link(self, number):
        self.driver.find_elements_by_css_selector(self.EDIT_LINK)[number].click()

    def click_on_delete_good_button(self):
        self.driver.find_element_by_css_selector(self.DELETE_BUTTON).click()

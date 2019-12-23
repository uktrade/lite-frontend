from selenium.webdriver.support.ui import Select

from shared import functions


class ApplicationGoodsList:
    def __init__(self, driver, prefix=""):
        self.driver = driver
        self.prefix = prefix
        self.add_new_good_button = "add-new"  # ID
        self.quantity_field = "quantity"  # ID
        self.unit_dropdown = "unit"  # ID
        self.value_field = "value"  # ID
        self.filter_description_search_box = "description"  # ID
        self.filter_part_number_search_box = "part_number"  # ID
        self.filter_control_rating_search_box = "control_rating"  # ID
        self.filter_button = "button-apply-filters"  # ID
        self.card_label = ".lite-card .govuk-label"
        self.part_number = "good-part-number"
        self.show_filters_link = "show-filters-link"  # ID
        self.description = "good-description"
        self.control_code = "good-control_code"
        self.good_entry = ".govuk-table__body .govuk-table__row"

    def add_values_to_good(self, value, quantity, unit):
        self.driver.find_element_by_id(self.prefix + self.value_field).send_keys(value)
        self.driver.find_element_by_id(self.prefix + self.quantity_field).send_keys(quantity)
        select = Select(self.driver.find_element_by_id(self.prefix + self.unit_dropdown))
        select.select_by_visible_text(unit)

    def click_on_overview(self):
        functions.click_back_link(self.driver)

    def type_into_filter_description_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.show_filters_link).click()
        self.driver.find_element_by_id(self.filter_description_search_box).send_keys(value)
        self.driver.find_element_by_id(self.filter_button).click()

    def type_into_filter_part_number_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_part_number_search_box).send_keys(value)
        self.driver.find_element_by_id(self.filter_button).click()

    def type_into_filter_control_rating_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_control_rating_search_box).send_keys(value)
        self.driver.find_element_by_id(self.filter_button).click()

    def get_good_descriptions(self):
        return self.driver.find_elements_by_id(self.description)

    def get_good_part_numbers(self):
        return self.driver.find_elements_by_id(self.part_number)

    def get_good_control_codes(self):
        return self.driver.find_elements_by_id(self.control_code)

    def click_add_new_good_button(self):
        return self.driver.find_element_by_id(self.add_new_good_button).click()

    def get_goods_count(self):
        return len(self.driver.find_elements_by_css_selector(self.good_entry))

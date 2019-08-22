from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class ApplicationGoodsList:

    def __init__(self, driver):
        self.driver = driver
        self.add_from_org_goods_button = 'a.govuk-button[href*="add_preexisting"]'   # CSS
        self.add_to_application = 'a.govuk-button'
        self.overview_link = '.govuk-back-link'   # CSS
        self.quantity_field = 'quantity'   # ID
        self.unit_dropdown = 'unit'   # ID
        self.value_field = 'value'   # ID
        self.filter_description_search_box = 'description'   # ID
        self.filter_part_number_search_box = 'part_number'   # ID
        self.filter_control_rating_search_box = 'control_rating'   # ID
        self.filter_button = '//button[text()[contains(.,"Filter")]]' #xpath
        self.goods_items = '.lite-card'   # CSS
        self.filter_tags = ".lite-filter-bar a"

    def click_add_from_organisations_goods_button(self):
        return self.driver.find_element_by_css_selector(self.add_from_org_goods_button).click()

    def click_add_to_application(self, no):
        return self.driver.find_elements_by_css_selector(self.add_to_application)[no-1].click()

    def add_values_to_good(self, value, quantity, unit):
        self.driver.find_element_by_id(self.value_field).send_keys(value)
        self.driver.find_element_by_id(self.quantity_field).send_keys(quantity)
        select = Select(self.driver.find_element_by_id(self.unit_dropdown))
        select.select_by_visible_text(unit)

    def click_on_overview(self):
        self.driver.find_element_by_css_selector(self.overview_link).click()

    def type_into_filter_description_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_description_search_box).send_keys(value)
        self.driver.find_element_by_xpath(self.filter_button).click()

    def type_into_filter_part_number_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_part_number_search_box).send_keys(value)
        self.driver.find_element_by_xpath(self.filter_button).click()

    def type_into_filter_control_rating_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_control_rating_search_box).send_keys(value)
        self.driver.find_element_by_xpath(self.filter_button).click()

    def get_size_of_goods(self):
        return len(self.driver.find_elements_by_css_selector(self.goods_items))

    def get_text_of_good(self, no):
        return self.driver.find_elements_by_css_selector(self.goods_items)[no].text

    def get_tag_name_of_good(self, no):
        return self.driver.find_elements_by_css_selector(self.goods_items)[no].find_element(By.TAG_NAME, "h4").text

    def remove_filters(self):
        for tag in range(len(self.driver.find_elements_by_css_selector(self.filter_tags))):
            self.driver.find_elements_by_css_selector(self.filter_tags)[tag-1].click()

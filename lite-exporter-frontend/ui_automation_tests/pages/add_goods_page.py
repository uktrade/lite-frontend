class AddGoodPage():

    def __init__(self, driver):
        self.driver = driver
        self.add_a_good_btn = "a[href*='/goods/add/']"


    def click_add_a_good(self):
        self.driver.find_element_by_css_selector(self.add_a_good_btn).click()

    def enter_description_of_goods(self, description):
        description_tb = self.driver.find_element_by_id("description")
        description_tb.clear()
        description_tb.send_keys(description)

    def select_is_your_good_controlled(self, option):
        if option == "Yes":
            self.driver.find_element_by_id("is_good_controlled-yes").click()
        else:
            self.driver.find_element_by_id("is_good_controlled-no").click()

    def enter_control_code(self, code):
        control_code_tb = self.driver.find_element_by_id("control_code")
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def select_is_your_good_intended_to_be_incorporated_into_an_end_product(self, option):
        if option == "Yes":
            self.driver.find_element_by_id("is_good_end_product-yes").click()
        else:
            self.driver.find_element_by_id("is_good_end_product-no").click()

    def enter_part_number(self, part_number):
        part_number_tb = self.driver.find_element_by_id("part_number")
        part_number_tb.clear()
        part_number_tb.send_keys(part_number)

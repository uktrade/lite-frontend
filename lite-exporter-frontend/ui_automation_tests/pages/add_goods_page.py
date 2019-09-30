class AddGoodPage:

    def __init__(self, driver):
        self.driver = driver
        self.add_a_good_btn = "#add-a-good"

    def click_add_a_good(self):
        self.driver.find_element_by_css_selector(self.add_a_good_btn).click()

    def enter_description_of_goods(self, description):
        description_tb = self.driver.find_element_by_id("description")
        description_tb.clear()
        description_tb.send_keys(description)

    def select_is_your_good_controlled(self, option):
        # The only options accepted here are 'yes', 'no' and 'unsure'
        self.driver.find_element_by_id("is_good_controlled-%s" % option.lower()).click()

    def enter_control_code(self, code):
        control_code_tb = self.driver.find_element_by_id("control_code")
        control_code_tb.clear()
        control_code_tb.send_keys(code)

        # This is done as control code textbox needs to lose focus
        self.driver.find_element_by_tag_name('body').click()

    def enter_control_code_unsure(self, code):
        control_code_tb = self.driver.find_element_by_id("not_sure_details_control_code")
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def enter_control_unsure_details(self, details):
        unsure_details = self.driver.find_element_by_id("not_sure_details_details")
        unsure_details.clear()
        unsure_details.send_keys(details)

    def select_control_unsure_confirmation(self, option):
        # The only options accepted here are 'yes' and 'no
        self.driver.find_element_by_id("clc_query_confirmation-" + option.lower()).click()

    def select_is_your_good_intended_to_be_incorporated_into_an_end_product(self, option):
        if option == "Yes":
            self.driver.find_element_by_id("is_good_end_product-no").click()
        else:
            self.driver.find_element_by_id("is_good_end_product-yes").click()

    def enter_part_number(self, part_number):
        part_number_tb = self.driver.find_element_by_id("part_number")
        part_number_tb.clear()
        part_number_tb.send_keys(part_number)

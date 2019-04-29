from selenium.webdriver.common.by import By
import helpers.helpers as utils
import pytest

class ExporterHubPage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.apply_for_a_licence_btn = "a[href*='/new-application/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.applications_btn = "a[href*='/applications/']"
        self.my_goods_btn = "a[href*='/goods/']"
        self.add_a_good_btn = "a[href*='/goods/add/']"

    def go_to(self, url):
        self.driver.get(url)

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.apply_for_a_licence_btn).click()

    def click_drafts(self):
        self.driver.find_element_by_css_selector(self.drafts_btn).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.applications_btn).click()

    def enter_email(self, email):
        email_tb = self.driver.find_element_by_id("email")
        email_tb.clear()
        email_tb.send_keys(email)

    def enter_password(self, password):
        password_tb = self.driver.find_element_by_id("password")
        password_tb.send_keys(password)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()

    def click_submit(self):
        self.driver.find_element_by_css_selector(".govuk-button").click()

    def click_my_goods(self):
        self.driver.find_element_by_css_selector(self.my_goods_btn).click()

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

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[action*='submit']").click()

    def verify_good_is_in_goods_list(self, description, part_number, control_code):
        goods_row = self.driver.find_element_by_xpath("//*[text()[contains(.,'" + description + "')]]")
        assert goods_row.is_displayed()
        assert goods_row.find_element_by_xpath(".//following-sibling::td").text == part_number
        assert goods_row.find_element_by_xpath(".//following-sibling::td[2]").text == control_code

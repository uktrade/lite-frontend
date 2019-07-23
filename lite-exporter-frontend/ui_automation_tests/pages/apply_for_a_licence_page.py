from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import helpers.helpers as utils

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

class ApplyForALicencePage:

    def __init__(self, driver):
        self.driver = driver

        self.apply_for_a_licence_btn = "a[href*='/apply_for_a_licence/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.name_or_reference_input_id = "name"
        self.control_code_input_id = "control_code"
        self.destination_input_id = "destination"
        self.usage_input_id = "usage"
        self.activity_input_id = "activity"
        self.standard_licence_button = "input#licence_type-standard_licence"
        self.open_licence_button = "input#licence_type-open_licence"
        self.submit_button = "button[type*='submit']"
        self.export_button = "export_type-"
        self.export_licence_yes_or_no = "have_you_been_informed-"
        self.reference_number = "reference_number_on_information_form"
        self.licence_application_headers = ".govuk-table__header"
        self.success_message = ".govuk-panel__title"
        self.licence_application_values = ".govuk-table__cell"
        self.start_now_btn = "a[href*='/start']"
        self.application_is_submitted = '.govuk-panel__title'
        self.delete_application_button = '.cancel-link' #css

    def enter_name_or_reference_for_application(self, name):
        self.driver.find_element_by_id(self.name_or_reference_input_id).clear()
        self.driver.find_element_by_id(self.name_or_reference_input_id).send_keys(name)

    def enter_control_code(self, control_code):
        self.driver.find_element_by_id(self.control_code_input_id).clear()
        self.driver.find_element_by_id(self.control_code_input_id).send_keys(control_code)

    def enter_destination(self, destination):
        self.driver.find_element_by_id(self.destination_input_id).clear()
        self.driver.find_element_by_id(self.destination_input_id).send_keys(destination)

    def enter_usage(self, usage):
        self.driver.find_element_by_id(self.usage_input_id).clear()
        self.driver.find_element_by_id(self.usage_input_id).send_keys(usage)

    def enter_activity(self, activity):
        self.driver.find_element_by_id(self.activity_input_id).clear()
        self.driver.find_element_by_id(self.activity_input_id).send_keys(activity)

    def click_start_now_btn(self):
        self.driver.find_element_by_css_selector(self.start_now_btn).click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_continue(self):
        self.click_save_and_continue()

    def click_go_to_overview(self):
        self.driver.find_element_by_xpath("//a[text()[contains(.,'Overview')]]").click()

    def click_delete_application(self):
        self.driver.find_element_by_css_selector(self.delete_application_button).click()
        self.driver.implicitly_wait(10)
        self.driver.execute_script("document.querySelectorAll('.govuk-button--warning')[0].click()")

    def click_submit_application(self):
        self.driver.execute_script("document.querySelectorAll(\"button[type*='submit']\")[0].click()")

    def click_goods_link(self):
        self.driver.find_element_by_xpath("//a[text()='Goods']").click()

    def click_add_from_organisations_goods(self):
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Add from organisations goods')]]").click()

    def add_good_to_application(self, des):
        good = self.driver.find_element_by_xpath("//div[@class='lite-card']/h4[text()='" + des + "']")
        # goods = self.driver.find_elements_by_xpath("//div[@class='lite-card']")
        # for good in goods:
        #     if good.find_element(By.TAG_NAME, "h4").text == des:
        good.find_element(By.XPATH, "./following::div[1]/a[text()='Add to application']").click()

    def enter_quantity(self, qty):
        self.driver.find_element_by_id("quantity").clear()
        self.driver.find_element_by_id("quantity").send_keys(qty)

    def enter_value(self, value):
        self.driver.find_element_by_id("value").clear()
        self.driver.find_element_by_id("value").send_keys(value)

    def select_unit_of_measurement(self, unit):
        select = Select(self.driver.find_element_by_id('unit'))
        select.select_by_visible_text(unit)

    def enter_description(self, description):
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(description)

    def enter_part_number(self, part_number):
        self.driver.find_element_by_id("part_number").clear()
        self.driver.find_element_by_id("part_number").send_keys(part_number)

    def click_filter_btn(self):
        self.driver.find_element_by_xpath("//button[text()[contains(.,'Filter')]]").click()

    def click_export_licence(self, type):
        logging.info(type)
        if (type == "standard"):
            return self.driver.find_element_by_css_selector(self.standard_licence_button).click()
        elif (type == "open"):
            return self.driver.find_element_by_css_selector(self.open_licence_button).click()

    def click_permanent_or_temporary_button(self, string):
        self.driver.find_element_by_id(self.export_button + string).click()

    def click_export_licence_yes_or_no(self, string):
        self.driver.find_element_by_id(self.export_licence_yes_or_no + string).click()

    def get_text_of_application_results(self, no):
        return self.driver.find_elements_by_css_selector(self.licence_application_values)[no].text

    def get_text_of_application_headers(self, no):
        utils.highlight(self.driver.find_elements_by_css_selector(self.licence_application_headers)[no])
        return self.driver.find_elements_by_css_selector(self.licence_application_headers)[no].text

    def get_text_of_success_message(self):
        return self.driver.find_element_by_css_selector(self.success_message).text

    def type_into_reference_number(self, string):
        self.driver.find_element_by_id(self.reference_number).send_keys(string)

    def enter_application_details_new(self, name, licence_type, temp_or_perm, need_licence, ref_number):
        self.enter_name_or_reference_for_application(name)
        self.click_save_and_continue()
        self.click_export_licence(licence_type)
        self.click_continue()
        self.click_permanent_or_temporary_button(temp_or_perm)
        self.click_continue()
        self.click_export_licence_yes_or_no(need_licence)
        self.type_into_reference_number(ref_number)

    def application_submitted_text(self):
        return self.driver.find_element_by_css_selector(self.application_is_submitted).text

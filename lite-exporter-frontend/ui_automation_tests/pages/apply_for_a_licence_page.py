from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class ApplyForALicencePage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.apply_for_a_licence_btn = "a[href*='/new-application/']"
        self.drafts_btn = "a[href*='/drafts/']"
        self.name_or_reference_input_id = "name"
        self.control_code_input_id = "control_code"
        self.destination_input_id = "destination"
        self.usage_input_id = "usage"
        self.activity_input_id = "activity"

    def enter_name_or_reference_for_application(self, name):
        self.driver.find_element_by_id(self.name_or_reference_input_id).clear()
        self.driver.find_element_by_id(self.name_or_reference_input_id).send_keys(name)

    def enter_control_code(self, controlCode):
        self.driver.find_element_by_id(self.control_code_input_id).clear()
        self.driver.find_element_by_id(self.control_code_input_id).send_keys(controlCode)

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
        self.driver.find_element_by_css_selector("a[href*='/start']").click()

    def click_save_and_continue(self):
        self.driver.find_element_by_css_selector("button[action*='submit']").click()

    def click_go_to_overview(self):
        self.driver.find_element_by_xpath("//a[text()[contains(.,'Overview')]]").click()

    def click_delete_application(self):
        self.driver.find_element_by_css_selector(".cancel-link").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_css_selector("#modal-contents a.govuk-button.govuk-button--warning").click()

    def click_submit_application(self):
        self.driver.find_element_by_css_selector("button[type*='submit']").click()

    def click_goods_link(self):
        self.driver.find_element_by_xpath("//a[text()='Goods']").click()

    def click_add_from_organisations_goods(self):
        self.driver.find_element_by_xpath("//*[text()[contains(.,'Add from organisations goods')]]").click()

    def add_good_to_application(self, des):
        good = self.driver.find_element_by_xpath("//div[@class='lite-item']/h4[text()='" + des + "']")
        # goods = self.driver.find_elements_by_xpath("//div[@class='lite-item']")
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



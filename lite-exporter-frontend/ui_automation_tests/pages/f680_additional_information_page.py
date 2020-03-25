from selenium.webdriver.remote.webdriver import WebDriver

from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class F680AdditionalInformationPage(BasePage):
    DATE_DAY_ID = "day"
    DATE_MONTH_ID = "month"
    DATE_YEAR_ID = "year"
    # Summary list buttons
    EXPEDITED_ID = "expedited"
    FOREIGN_TECHNOLOGY_ID = "foreign_technology"
    LOCALLY_MANUFACTURED_ID = "locally_manufactured"
    ELECTRONIC_WARFARE_REQUIREMENT_ID = "electronic_warfare_requirement"
    MTCR_TYPE_ID = "mtcr_type"
    UK_SERVICE_EQUIPMENT_ID = "uk_service_equipment"
    UK_SERVICE_EQUIPMENT_TYPE_ID = "uk_service_equipment_type"
    PROSPECT_VALUE_ID = "prospect_value"
    # Value setters
    EXPEDITED_SELECTOR_ID = "expedited-{value}"
    FOREIGN_TECHNOLOGY_SELECTOR_ID = "foreign_technology-{value}"
    LOCALLY_MANUFACTURED_SELECTOR_ID = "locally_manufactured-{value}"
    ELECTRONIC_WARFARE_REQUIREMENT_SELECTOR_ID = "electronic_warfare_requirement-{value}"
    MTCR_TYPE_SELECTOR_ID = "mtcr_type-{value}"
    UK_SERVICE_EQUIPMENT_SELECTOR_ID = "uk_service_equipment-{value}"
    UK_SERVICE_EQUIPMENT_TYPE_SELECTOR_ID = "uk_service_equipment_type-{value}"
    PROSPECT_VALUE_SELECTOR_ID = "prospect_value"

    def __init__(self, driver: WebDriver, submit_button_value: str):
        """
        Summary list forms use `submit` value for buttons in initial flow, and `return` when editing individual values
        """
        super().__init__(driver=driver)
        self.submit_button_value = submit_button_value

    def enter_date_of_issue(self, day, month, year):
        self.driver.find_element_by_id(self.DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.DATE_YEAR_ID).send_keys(year)
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_no_date(self, value=False):
        self.driver.find_element_by_id(self.EXPEDITED_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_foreign_technology(self, value=False):
        self.driver.find_element_by_id(self.FOREIGN_TECHNOLOGY_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_locally_manufactured(self, value=False):
        self.driver.find_element_by_id(self.LOCALLY_MANUFACTURED_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_mtcr_type(self, value="mtcr_category_2"):
        self.driver.find_element_by_id(self.MTCR_TYPE_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_electronic_warfare_requirement(self, value=False):
        self.driver.find_element_by_id(self.ELECTRONIC_WARFARE_REQUIREMENT_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_uk_service_equipment(self, value=False):
        self.driver.find_element_by_id(self.UK_SERVICE_EQUIPMENT_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_uk_service_equipment_type(self, value="mod_funded"):
        self.driver.find_element_by_id(self.UK_SERVICE_EQUIPMENT_TYPE_SELECTOR_ID.format(value=value)).click()
        functions.click_submit(self.driver, self.submit_button_value)

    def enter_prospect_value(self, value="100.00"):
        functions.enter_value(self.driver, element_id=self.PROSPECT_VALUE_SELECTOR_ID, value=value)
        functions.click_submit(self.driver, self.submit_button_value)

    def click_expedited(self):
        self.driver.find_element_by_id(self.EXPEDITED_ID).click()

    def click_foreign_technology(self):
        self.driver.find_element_by_id(self.FOREIGN_TECHNOLOGY_ID).click()

    def click_locally_manufactured(self):
        self.driver.find_element_by_id(self.LOCALLY_MANUFACTURED_ID).click()

    def click_mtcr_type(self):
        self.driver.find_element_by_id(self.MTCR_TYPE_ID).click()

    def click_electronic_warfare_requirement(self):
        self.driver.find_element_by_id(self.ELECTRONIC_WARFARE_REQUIREMENT_ID).click()

    def click_uk_service_equipment(self):
        self.driver.find_element_by_id(self.UK_SERVICE_EQUIPMENT_ID).click()

    def click_uk_service_equipment_type(self):
        self.driver.find_element_by_id(self.UK_SERVICE_EQUIPMENT_TYPE_ID).click()

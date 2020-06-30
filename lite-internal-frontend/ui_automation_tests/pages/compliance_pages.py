from selenium.webdriver.support.select import Select
from shared.BasePage import BasePage

from shared import functions

from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id


class CompliancePages(BasePage):

    CASE_REFERENCE_ID = "reference"
    COMPLIANCE_BANNER_DETAILS = "candy-visit-date"
    ADD_VISIT_REPORT_ID = "add-visit-report"
    EDIT_VISIT_REPORT_DETAILS_ID = "edit-visit-report-details"
    VISIT_TYPE_ID = "visit_type"
    VISIT_DATE_ID = "visit_date"
    VISIT_DATE_DAY_ID = "visit_date_day"
    VISIT_DATE_MONTH_ID = "visit_date_month"
    VISIT_DATE_YEAR_ID = "visit_date_year"
    OVERALL_RISK_VALUE_ID = "overall_risk_value"
    LICENCE_RISK_VALUE_ID = "licence_risk_value"
    EDIT_OVERVIEW_ID = "edit-overview"
    OVERVIEW_ID = "overview"
    EDIT_INSPECTION_ID = "edit-inspection"
    INSPECTION_ID = "inspection"
    EDIT_COMPLIANCE_WITH_LICENCES_ID = "edit-compliance-with-licences"
    COMPLIANCE_WITH_LICENCE_OVERVIEW_ID = "compliance_overview"
    COMPLIANCE_WITH_LICENCE_RISK_VALUE_ID = "compliance_risk_value"
    EDIT_KNOWLEDGE_OF_INDIVIDUALS_ID = "edit-knowledge-of-individuals"
    KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID = "individuals_overview"
    KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID = "individuals_risk_value"
    EDIT_KNOWLEDGE_OF_PRODUCTS_ID = "edit-knowledge-of-products"
    KNOWLEDGE_OF_PRODUCTS_OVERVIEW_ID = "products_overview"
    KNOWLEDGE_OF_PRODUCTS_RISK_VALUE_ID = "products_risk_value"

    ADD_PEOPLE_PRESENT_BUTTON = "add-people-present"
    ADD_PERSON_BUTTON_ID = "button-add-person"
    PERSON_NAME_ID = "name-1"
    PERSON_JOB_TITLE_ID = "job-title-1"
    PEOPLE_PRESENT_TABLE_ID = "people_present"

    def find_case_reference(self, context):
        return self.driver.find_element_by_link_text(context.reference_code)

    def filter_by_case_reference(self, context):
        self.driver.find_element_by_id(self.CASE_REFERENCE_ID).send_keys(context.reference_code)

    def add_visit_report(self):
        self.driver.find_element_by_id(self.ADD_VISIT_REPORT_ID).click()

    def add_visit_report_details(self, visit_type, visit_date, overall_risk, licence_risk):
        scroll_to_element_by_id(self.driver, self.EDIT_VISIT_REPORT_DETAILS_ID)
        self.driver.find_element_by_id(self.EDIT_VISIT_REPORT_DETAILS_ID).click()
        Select(self.driver.find_element_by_id(self.VISIT_TYPE_ID)).select_by_visible_text(visit_type)

        year, month, day = visit_date.split("-")
        self.driver.find_element_by_id(self.VISIT_DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.VISIT_DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.VISIT_DATE_YEAR_ID).send_keys(year)

        Select(self.driver.find_element_by_id(self.OVERALL_RISK_VALUE_ID)).select_by_visible_text(overall_risk)

        Select(self.driver.find_element_by_id(self.LICENCE_RISK_VALUE_ID)).select_by_visible_text(licence_risk)

        functions.click_submit(self.driver)

    def get_visit_type(self):
        return self.driver.find_element_by_id(self.VISIT_TYPE_ID).text

    def get_visit_date(self):
        return self.driver.find_element_by_id(self.VISIT_DATE_ID).text

    def get_overall_risk(self):
        return self.driver.find_element_by_id(self.OVERALL_RISK_VALUE_ID).text

    def get_licence_risk(self):
        return self.driver.find_element_by_id(self.LICENCE_RISK_VALUE_ID).text

    def edit_overview(self, text):
        scroll_to_element_by_id(self.driver, self.EDIT_OVERVIEW_ID)
        self.driver.find_element_by_id(self.EDIT_OVERVIEW_ID).click()
        self.driver.find_element_by_id(self.OVERVIEW_ID).send_keys(text)
        functions.click_submit(self.driver)

    def get_overview(self):
        return self.driver.find_element_by_id(self.OVERVIEW_ID).text

    def edit_inspection(self, text):
        scroll_to_element_by_id(self.driver, self.EDIT_INSPECTION_ID)
        self.driver.find_element_by_id(self.EDIT_INSPECTION_ID).click()
        self.driver.find_element_by_id(self.INSPECTION_ID).send_keys(text)
        functions.click_submit(self.driver)

    def get_inspection(self):
        return self.driver.find_element_by_id(self.INSPECTION_ID).text

    def edit_compliance_with_licences(self, overview, risk_value):
        scroll_to_element_by_id(self.driver, self.EDIT_COMPLIANCE_WITH_LICENCES_ID)
        self.driver.find_element_by_id(self.EDIT_COMPLIANCE_WITH_LICENCES_ID).click()
        self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_OVERVIEW_ID).send_keys(overview)
        Select(self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_RISK_VALUE_ID)).select_by_visible_text(
            risk_value
        )
        functions.click_submit(self.driver)

    def get_compliance_with_licence_overview(self):
        return self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_OVERVIEW_ID).text

    def get_compliance_with_licence_risk(self):
        return self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_RISK_VALUE_ID).text

    def edit_knowledge_of_individuals(self, overview, risk_value):
        scroll_to_element_by_id(self.driver, self.EDIT_KNOWLEDGE_OF_INDIVIDUALS_ID)
        self.driver.find_element_by_id(self.EDIT_KNOWLEDGE_OF_INDIVIDUALS_ID).click()
        self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID).send_keys(overview)
        Select(self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID)).select_by_visible_text(
            risk_value
        )
        functions.click_submit(self.driver)

    def get_knowledge_of_individuals_overview(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID).text

    def get_knowledge_of_individuals_risk(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID).text

    def edit_knowledge_of_products(self, overview, risk_value):
        scroll_to_element_by_id(self.driver, self.EDIT_KNOWLEDGE_OF_PRODUCTS_ID)
        self.driver.find_element_by_id(self.EDIT_KNOWLEDGE_OF_PRODUCTS_ID).click()
        self.driver.find_element_by_id(self.KNOWLEDGE_OF_PRODUCTS_OVERVIEW_ID).send_keys(overview)
        Select(self.driver.find_element_by_id(self.KNOWLEDGE_OF_PRODUCTS_RISK_VALUE_ID)).select_by_visible_text(
            risk_value
        )
        functions.click_submit(self.driver)

    def get_knowledge_of_products_overview(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_PRODUCTS_OVERVIEW_ID).text

    def get_knowledge_of_products_risk(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_PRODUCTS_RISK_VALUE_ID).text

    def add_person_present(self, name, job_title):
        scroll_to_element_by_id(self.driver, self.ADD_PEOPLE_PRESENT_BUTTON)
        self.driver.find_element_by_id(self.ADD_PEOPLE_PRESENT_BUTTON).click()
        self.driver.find_element_by_id(self.ADD_PERSON_BUTTON_ID).click()
        self.driver.find_element_by_id(self.PERSON_NAME_ID).send_keys(name)
        self.driver.find_element_by_id(self.PERSON_JOB_TITLE_ID).send_keys(job_title)
        functions.click_submit(self.driver)

    def get_people_present_table(self):
        return self.driver.find_element_by_id(self.PEOPLE_PRESENT_TABLE_ID).text

    def get_compliance_banner_details(self):
        return self.driver.find_element_by_id(self.COMPLIANCE_BANNER_DETAILS).text

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.exporter.pages.BasePage import BasePage


class AddGoodGradingPage(BasePage):

    PREFIX_ID = "prefix"
    GRADING_ID = "grading"
    SUFFIX_ID = "suffix"
    ISSUING_AUTHORITY_ID = "issuing_authority"
    REFERENCE_ID = "reference"
    DATE_OF_ISSUE_DAY_ID = "date_of_issueday"
    DATE_OF_ISSUE_MONTH_ID = "date_of_issuemonth"
    DATE_OF_ISSUE_YEAR_ID = "date_of_issueyear"

    def enter_prefix_of_goods_grading(self, prefix):
        self.driver.find_element(by=By.ID, value=self.PREFIX_ID).send_keys(prefix)

    def enter_good_grading(self, grading):
        Select(self.driver.find_element(by=By.ID, value=self.GRADING_ID)).select_by_value(grading)

    def enter_suffix_of_goods_grading(self, suffix):
        self.driver.find_element(by=By.ID, value=self.SUFFIX_ID).send_keys(suffix)

    def enter_issuing_authority(self, issuing_authority):
        self.driver.find_element(by=By.ID, value=self.ISSUING_AUTHORITY_ID).send_keys(issuing_authority)

    def enter_reference(self, reference):
        self.driver.find_element(by=By.ID, value=self.REFERENCE_ID).send_keys(reference)

    def enter_date_of_issue(self, day, month, year):
        self.driver.find_element(by=By.ID, value=self.DATE_OF_ISSUE_DAY_ID).send_keys(day)
        self.driver.find_element(by=By.ID, value=self.DATE_OF_ISSUE_MONTH_ID).send_keys(month)
        self.driver.find_element(by=By.ID, value=self.DATE_OF_ISSUE_YEAR_ID).send_keys(year)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests_common import functions
from django.conf import settings
from ui_tests.caseworker.pages.BasePage import BasePage


class ProductAssessmentPage(BasePage):
    def assess_rating(self, rating):
        functions.select_multi_select_options(
            self.driver,
            "#div_id_control_list_entries .lite-autocomplete__input",
            [rating],
        )

    def check_product_not_on_control_list(self):
        element = self.driver.find_element(by=By.ID, value="id_does_not_have_control_list_entries")
        element.click()

    def assess_report_summary_prefix(self, ars_prefix):
        ars_prefix_element = self.driver.find_element(by=By.ID, value="report_summary_prefix_container")
        ars_prefix_input = ars_prefix_element.find_element(by=By.ID, value="_report_summary_prefix")
        ars_prefix_input.send_keys(ars_prefix)
        WebDriverWait(self.driver, 30 * settings.E2E_WAIT_MULTIPLIER).until(
            expected_conditions.presence_of_element_located((By.ID, "_report_summary_prefix__listbox"))
        )

        suggestions_list = self.driver.find_element(by=By.ID, value="_report_summary_prefix__listbox")

        # select from the suggestions
        for element in suggestions_list.find_elements(by=By.CLASS_NAME, value="govuk-body"):
            if element.text == ars_prefix:
                ars_prefix_input.send_keys(Keys.RETURN)
                break

    def assess_report_summary_subject(self, ars_subject):
        ars_subject_element = self.driver.find_element(by=By.ID, value="report_summary_subject_container")
        ars_subject_input = ars_subject_element.find_element(by=By.ID, value="_report_summary_subject")
        ars_subject_input.send_keys(ars_subject)
        WebDriverWait(self.driver, 30 * settings.E2E_WAIT_MULTIPLIER).until(
            expected_conditions.presence_of_element_located((By.ID, "_report_summary_subject__listbox"))
        )

        suggestions_list = self.driver.find_element(by=By.ID, value="_report_summary_subject__listbox")

        # select from the suggestions
        for element in suggestions_list.find_elements(by=By.CLASS_NAME, value="govuk-body"):
            if element.text == ars_subject:
                ars_subject_input.send_keys(Keys.RETURN)
                break

    def mark_regime_none(self):
        parent_div = self.driver.find_element(by=By.CLASS_NAME, value="govuk-checkboxes--conditional")
        check_box_divs = parent_div.find_elements(by=By.CLASS_NAME, value="govuk-checkboxes__item")

        # find checkbox related to given regime
        for item in check_box_divs:
            if item.text == "None":
                input_element = item.find_element(by=By.CLASS_NAME, value="govuk-checkboxes__input")
                input_element.click()
                break

    def add_assessment_note(self, comment):
        assessment_note = self.driver.find_element(by=By.ID, value="id_comment")
        assessment_note.clear()
        assessment_note.send_keys(comment)

    def check_product_assessment_status(self, name):
        assessed_products = []
        header = self.driver.find_elements(by=By.XPATH, value='//*[@id="tau-form"]/thead/tr')
        headings = [item.text for item in header[0].find_elements(by=By.TAG_NAME, value="th")]

        for row in self.driver.find_elements(by=By.XPATH, value='//*[@id="tau-form"]/tbody/tr'):
            row_data = [item.text for item in row.find_elements(by=By.TAG_NAME, value="td")]
            product = {k: v for k, v in zip(headings, row_data)}
            assessed_products.append(product)

        for product in assessed_products:
            if product["Name and part number"] == name:
                break
        else:
            raise ValueError(f"Product {name} not in list of assessed products")

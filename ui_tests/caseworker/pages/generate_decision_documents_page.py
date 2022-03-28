from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.functions import element_with_id_exists


class GeneratedDecisionDocuments(BasePage):
    DECISION_ROW_PARTIAL_ID = "decision-"
    GENERATE_BUTTON_PARTIAL_ID = "generate-document-"
    DECISION_ROW_STATUS_PARTIAL_ID = "status-"

    def decision_row_exists(self, decision_key):
        return element_with_id_exists(self.driver, self.DECISION_ROW_PARTIAL_ID + decision_key)

    def click_generate_decision_document(self, decision_key):
        self.driver.find_element_by_id(self.GENERATE_BUTTON_PARTIAL_ID + decision_key).click()

    def get_section_status(self, decision_key):
        return self.driver.find_element_by_id(self.DECISION_ROW_STATUS_PARTIAL_ID + decision_key).get_attribute(
            "data-status"
        )

    def get_decision_document_name(self):
        return self.driver.find_element(
            by=By.XPATH, value=f"//th[ancestor::tr[contains(@id, 'decision-')]]"
        ).text.strip()

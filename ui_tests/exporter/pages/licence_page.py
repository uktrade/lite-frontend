from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage
from tests_common.functions import element_with_id_exists


class LicencePage(BasePage):
    HEADING_ID = "heading"
    LICENCE_DOCUMENT_DOWNLOAD_ID = "licence-document-download"
    DESTINATION_ID = "destination"
    END_USER_ID = "end-user"
    GOOD_ROW_ID = "good-row"
    USAGE_ID = "usage"

    def get_heading_text(self):
        return self.driver.find_element(by=By.ID, value=self.HEADING_ID).text

    def is_licence_document_present(self):
        return element_with_id_exists(self.driver, self.LICENCE_DOCUMENT_DOWNLOAD_ID)

    def get_destination(self):
        return self.driver.find_element(by=By.ID, value=self.DESTINATION_ID).text

    def get_end_user(self):
        return self.driver.find_element(by=By.ID, value=self.END_USER_ID).text

    def get_good_row(self):
        return self.driver.find_element(by=By.ID, value=self.GOOD_ROW_ID).text

    def get_usage(self):
        return self.driver.find_element(by=By.ID, value=self.USAGE_ID).text

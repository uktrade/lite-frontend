from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class EndUserPage(BasePage):
    DELETE_END_USER_DOCUMENT = "end_user_document_delete"  # ID

    def click_delete_end_user_document(self):
        self.driver.find_element(by=By.ID, value=self.DELETE_END_USER_DOCUMENT).click()

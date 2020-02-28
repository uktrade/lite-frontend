from ui_automation_tests.shared.BasePage import BasePage


class EndUserPage(BasePage):
    DELETE_END_USER_DOCUMENT = "end_user_document_delete"  # ID

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.DELETE_END_USER_DOCUMENT).click()

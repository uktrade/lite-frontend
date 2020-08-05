from ui_automation_tests.pages.BasePage import BasePage
from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id


class DeclarationPage(BasePage):
    FOI_ID = "agreed_to_foi-True"
    DECLARATION_ID = "agreed_to_declaration"
    CONDITION_OGEL_ID = "I-confirm-that-I've-read-the-licence-conditions-in-full"
    CONDITION_OGEL_EXPORT_ID = "I-confirm-that-my-export-complies-with-the-licence's-conditions-in-full"

    def agree_to_foi(self):
        scroll_to_element_by_id(self.driver, self.FOI_ID)
        self.driver.find_element_by_id(self.FOI_ID).click()

    def agree_to_declaration(self, driver):
        element = driver.find_element_by_css_selector("input[data-attribute='" + self.DECLARATION_ID + "']")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)

    def agree_to_ogel_conditions(self):
        self.driver.find_element_by_id(self.CONDITION_OGEL_ID).click()

    def agree_to_ogel_export_conditions(self):
        self.driver.find_element_by_id(self.CONDITION_OGEL_EXPORT_ID).click()

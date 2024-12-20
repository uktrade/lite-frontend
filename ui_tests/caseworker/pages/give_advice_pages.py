from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.helpers import scroll_to_element_below_header_by_id


class GiveAdvicePages(BasePage):
    ADVICE_CHECKBOX_OPTION = "type-"  # ID
    PICKLIST_ITEM_TEXT = ".lite-modal-content .app-picklist-picker__item"  # CSS
    TEXTAREA_NOTES_ID = "note"
    CLEARANCE_LEVEL_DROPDOWN_ID = "pv_grading_proviso"
    APPROVE_RADIO_ID = "approve."
    FOOTNOTE_REQUIRED_YES_RADIO_ID = "footnote_required-True"
    FOOTNOTE_REQUIRED_NO_RADIO_ID = "footnote_required-False"
    FOOTNOTE_TEXTBOX_ID = "footnote"

    def click_on_advice_option(self, option):
        self.driver.find_element(by=By.ID, value=self.ADVICE_CHECKBOX_OPTION + option).click()

    def click_on_import_link(self, option):
        scroll_to_element_below_header_by_id(self.driver, f"link-{option}-picklist-picker")
        self.driver.find_element(by=By.ID, value=f"link-{option}-picklist-picker").click()

    def click_on_picklist_item(self, option):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.PICKLIST_ITEM_TEXT).click()
        self.driver.execute_script('document.getElementById("button-submit-' + option + '").click()')

    def get_text_of_picklist_item(self):
        return self.driver.find_element(by=By.CSS_SELECTOR, value=self.PICKLIST_ITEM_TEXT).get_attribute("data-text")

    def type_in_additional_note_text_field(self, text):
        return self.driver.find_element(by=By.ID, value=self.TEXTAREA_NOTES_ID).send_keys(text)

    def checkbox_present(self):
        return len(self.driver.find_elements_by_css_selector(".input"))

    def clearance_grading_present(self):
        return self.driver.find_elements_by_id(self.CLEARANCE_LEVEL_DROPDOWN_ID)

    def select_clearance_grading(self, clearance_level):
        Select(self.driver.find_element(by=By.ID, value=self.CLEARANCE_LEVEL_DROPDOWN_ID)).select_by_visible_text(
            clearance_level
        )

    def select_footnote_required(self):
        self.driver.find_element(by=By.ID, value=self.FOOTNOTE_REQUIRED_YES_RADIO_ID).click()

    def select_footnote_not_required(self):
        self.driver.find_element(by=By.ID, value=self.FOOTNOTE_REQUIRED_NO_RADIO_ID).click()

    def enter_footnote(self, text):
        footnote_textbox = self.driver.find_element(by=By.ID, value=self.FOOTNOTE_TEXTBOX_ID)
        footnote_textbox.clear()
        footnote_textbox.send_keys(text)

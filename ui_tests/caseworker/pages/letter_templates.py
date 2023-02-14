from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.BasePage import BasePage


class LetterTemplates(BasePage):
    CREATE_TEMPLATE_BUTTON = "button-create-a-template"  # ID
    TEMPLATE_NAME = "name"  # ID
    LETTER_PARAGRAPH = "letter_paragraphs"  # NAME
    LETTER_PARAGRAPH_NAME = "letter_paragraph_name"  # NAME
    ADD_LETTER_PARAGRAPH_BUTTON = '[value="add_letter_paragraph"]'  # CSS
    ADD_LETTER_PARAGRAPHS_BUTTON = '[value="return_to_preview"]'  # CSS
    PREVIEW_BUTTON = "button-preview"  # ID
    PREVIEW = "preview"  # ID
    DRAG_DROP_LIST = "paragraphlist"  # ID
    DRAG_DROP_LIST_PARAGRAPH_TEXT = "paragraph-text"  # ID
    VISIBLE_TO_EXPORTER_PARTIAL_ID = "visible_to_exporter-"
    HAS_SIGNATURE_PARTIAL_ID = "include_digital_signature-"
    DONE_BUTTON_ID = "done"

    # Template page
    TEMPLATE_TITLE = "title"  # ID
    TEMPLATE_LAYOUT = "layout"  # ID
    CASE_TYPES = "case_types"  # ID
    TEMPLATE_PARAGRAPHS = "paragraph_content"  # ID
    EDIT_TEMPLATE_BUTTON = "edit_template"  # ID
    EDIT_PARAGRAPHS_BUTTON = "edit_template_paragraphs"  # ID
    ADD_PARAGRAPH_LINK = "add_paragraph"  # ID
    PARAGRAPH_CHECKBOXES_LIST = ".govuk-checkboxes__input"  # CSS

    def click_create_a_template(self):
        self.driver.find_element(by=By.ID, value=self.CREATE_TEMPLATE_BUTTON).click()

    def click_create_preview_button(self):
        self.driver.find_element(by=By.ID, value=self.PREVIEW_BUTTON).click()

    def enter_template_name(self, name):
        self.driver.find_element(by=By.ID, value=self.TEMPLATE_NAME).clear()
        self.driver.find_element(by=By.ID, value=self.TEMPLATE_NAME).send_keys(name)

    def select_which_type_of_cases_template_can_apply_to(self, id_selectors):
        for id_selector in id_selectors:
            self.driver.find_element(by=By.ID, value=id_selector).click()

    def select_which_type_of_decisions_template_can_apply_to(self, id_selectors):
        for id_selector in id_selectors:
            self.driver.find_element(by=By.ID, value=id_selector).click()

    def select_visible_to_exporter(self, value):
        self.driver.find_element(by=By.ID, value=self.VISIBLE_TO_EXPORTER_PARTIAL_ID + value).click()

    def select_has_signature(self, value):
        self.driver.find_element(by=By.ID, value=self.HAS_SIGNATURE_PARTIAL_ID + value).click()

    def click_licence_layout(self, template_id):
        self.driver.find_element(by=By.ID, value=template_id).click()

    def add_letter_paragraph(self):
        self.driver.find_element(by=By.NAME, value=self.LETTER_PARAGRAPH).click()
        return self.driver.find_element(by=By.NAME, value=self.LETTER_PARAGRAPH_NAME).text

    def click_add_letter_paragraph(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.ADD_LETTER_PARAGRAPH_BUTTON).click()

    def click_add_letter_paragraphs(self):
        self.driver.find_element(by=By.CSS_SELECTOR, value=self.ADD_LETTER_PARAGRAPHS_BUTTON).click()

    def get_text_in_template(self):
        return self.driver.find_element(by=By.ID, value=self.PREVIEW).text

    def get_paragraph_drag_and_drop_list_paragraph_text(self):
        return self.driver.find_element(by=By.ID, value=self.DRAG_DROP_LIST_PARAGRAPH_TEXT).text

    def get_paragraph_drag_and_drop_list_text(self):
        return self.driver.find_element(by=By.ID, value=self.DRAG_DROP_LIST).text

    def click_letter_template(self, document_template_name):
        Shared(self.driver).filter_by_name(document_template_name)
        self.driver.find_element(by=By.ID, value=document_template_name).click()

    def get_template_title(self):
        return self.driver.find_element(by=By.ID, value=self.TEMPLATE_TITLE).text

    def get_template_layout(self):
        return self.driver.find_element(by=By.ID, value=self.TEMPLATE_LAYOUT).text

    def get_template_case_types(self):
        return self.driver.find_element(by=By.ID, value=self.CASE_TYPES).text

    def get_template_paragraphs(self):
        return self.driver.find_element(by=By.ID, value=self.TEMPLATE_PARAGRAPHS).text

    def click_edit_template_button(self):
        self.driver.find_element(by=By.ID, value=self.EDIT_TEMPLATE_BUTTON).click()

    def click_edit_paragraphs_button(self):
        self.driver.find_element(by=By.ID, value=self.EDIT_PARAGRAPHS_BUTTON).click()

    def click_add_paragraph_link(self):
        self.driver.find_element(by=By.ID, value=self.ADD_PARAGRAPH_LINK).click()

    def get_add_paragraph_button(self):
        paragraph = self.driver.find_element(by=By.CSS_SELECTOR, value=self.PARAGRAPH_CHECKBOXES_LIST)
        id = paragraph.get_attribute("value")
        paragraph.click()
        return id

    def get_template_table_text(self):
        return Shared(self.driver).get_text_of_lite_table_body()

    def click_done_button(self):
        self.driver.find_element(by=By.ID, value=self.DONE_BUTTON_ID).click()

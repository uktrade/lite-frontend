from shared.BasePage import BasePage

from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.shared.tools.helpers import find_paginated_item_by_id, get_text_of_multi_page_table


class LetterTemplates(BasePage):
    CREATE_TEMPLATE_BUTTON = "button-create-a-template"  # ID
    TEMPLATE_NAME = "name"  # ID
    LETTER_PARAGRAPH = "letter_paragraphs"  # NAME
    LETTER_PARAGRAPH_NAME = "letter_paragraph_name"  # NAME
    ADD_LETTER_PARAGRAPH_BUTTON = '[value="add_letter_paragraph"]'  # CSS
    ADD_LETTER_PARAGRAPHS_BUTTON = '[value="return_to_preview"]'  # CSS
    PREVIEW_BUTTON = "button-preview"  # ID
    PREVIEW = "preview"  # ID
    DRAG_DROP_LIST = "standard-advice-list"  # ID
    PREVIEW_PARAGRAPHS = "paragraph-list"  # ID

    # Template page
    TEMPLATE_TITLE = "title"  # ID
    TEMPLATE_LAYOUT = "layout"  # ID
    CASE_TYPES = "case_types"  # ID
    TEMPLATE_PARAGRAPHS = "paragraph_content"  # ID
    EDIT_TEMPLATE_BUTTON = "edit_template"  # ID
    EDIT_PARAGRAPHS_BUTTON = "edit_template_paragraphs"  # ID
    ADD_PARAGRAPH_LINK = "add_paragraph"  # ID
    PARAGRAPH_CHECKBOXES_LIST = ".govuk-checkboxes__input"  # CSS
    PARAGRAPH_TEXT_LIST = "paragraph-list"  # ID

    def click_create_a_template(self):
        self.driver.find_element_by_id(self.CREATE_TEMPLATE_BUTTON).click()

    def click_create_preview_button(self):
        self.driver.find_element_by_id(self.PREVIEW_BUTTON).click()

    def enter_template_name(self, name):
        self.driver.find_element_by_id(self.TEMPLATE_NAME).clear()
        self.driver.find_element_by_id(self.TEMPLATE_NAME).send_keys(name)

    def select_which_type_of_cases_template_can_apply_to(self, id_selectors):
        for id_selector in id_selectors:
            self.driver.find_element_by_id(id_selector).click()

    def select_which_type_of_decisions_template_can_apply_to(self, id_selectors):
        for id_selector in id_selectors:
            self.driver.find_element_by_id(id_selector).click()

    def click_licence_layout(self, template_id):
        self.driver.find_element_by_id(template_id).click()

    def add_letter_paragraph(self):
        self.driver.find_element_by_name(self.LETTER_PARAGRAPH).click()
        return self.driver.find_element_by_name(self.LETTER_PARAGRAPH_NAME).text

    def click_add_letter_paragraph(self):
        self.driver.find_element_by_css_selector(self.ADD_LETTER_PARAGRAPH_BUTTON).click()

    def click_add_letter_paragraphs(self):
        self.driver.find_element_by_css_selector(self.ADD_LETTER_PARAGRAPHS_BUTTON).click()

    def get_text_in_template(self):
        return self.driver.find_element_by_id(self.PREVIEW).text

    def get_text_of_paragraphs_in_preview(self):
        return self.driver.find_element_by_id(self.PREVIEW_PARAGRAPHS).text

    def get_class_name_of_drag_and_drop_list(self):
        return self.driver.find_element_by_id(self.DRAG_DROP_LIST).get_attribute("class")

    def get_drag_and_drop_list_name(self):
        return self.driver.find_element_by_id(self.DRAG_DROP_LIST).text

    def click_letter_template(self, document_template_name):
        find_paginated_item_by_id(document_template_name, self.driver).click()

    def get_template_title(self):
        return self.driver.find_element_by_id(self.TEMPLATE_TITLE).text

    def get_template_layout(self):
        return self.driver.find_element_by_id(self.TEMPLATE_LAYOUT).text

    def get_template_case_types(self):
        return self.driver.find_element_by_id(self.CASE_TYPES).text

    def get_template_paragraphs(self):
        return self.driver.find_element_by_id(self.TEMPLATE_PARAGRAPHS).text

    def click_edit_template_button(self):
        self.driver.find_element_by_id(self.EDIT_TEMPLATE_BUTTON).click()

    def click_edit_paragraphs_button(self):
        self.driver.find_element_by_id(self.EDIT_PARAGRAPHS_BUTTON).click()

    def click_add_paragraph_link(self):
        self.driver.find_element_by_id(self.ADD_PARAGRAPH_LINK).click()

    def get_add_paragraph_button(self):
        paragraph = self.driver.find_element_by_css_selector(self.PARAGRAPH_CHECKBOXES_LIST)
        id = paragraph.get_attribute("value")
        paragraph.click()
        return id

    def get_list_of_letter_paragraphs(self):
        return self.driver.find_element_by_id(self.PARAGRAPH_TEXT_LIST).text

    def get_template_table_text(self):
        return get_text_of_multi_page_table(Shared.TABLE_CSS, self.driver)

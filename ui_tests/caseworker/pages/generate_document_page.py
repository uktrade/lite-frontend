from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.BasePage import BasePage
from tests_common.tools.helpers import find_paginated_item_by_id


class GeneratedDocument(BasePage):
    PREVIEW = "preview"  # ID
    PARAGRAPHS = "paragraph_content"  # ID
    LINK_DOWNLOAD_CLASS = "govuk-link--no-visited-state"
    TEXT = "text"  # ID
    PARAGRAPH_CHECKBOXES = ".govuk-checkboxes__input"  # CSS
    LINK_REGENERATE_ID = "regenerate"
    DOCUMENT_CLASS = "app-documents__item"
    ADDRESSEE_PARTIAL_ID = "addressee-"
    GENERATE_DECISION_DOCUMENT_BUTTON_ID = "generate-document-approve"
    DOCUMENT_TEMPLATE_CSS = ".govuk-label"

    def get_documents(self):
        return self.driver.find_elements_by_class_name(self.DOCUMENT_CLASS)

    def get_latest_document(self):
        return self.get_documents()[0]

    def click_letter_template(self, document_template_name):
        Shared(self.driver).go_to_last_page()
        self.driver.find_element_by_id(document_template_name).click()

    def select_addressee(self, id):
        find_paginated_item_by_id(self.ADDRESSEE_PARTIAL_ID + id, self.driver).click()

    def preview_is_shown(self):
        return self.driver.find_element_by_id(self.PREVIEW).is_displayed()

    def get_document_preview_text(self):
        return self.driver.find_element(by=By.ID, value=self.PREVIEW).text

    def get_document_paragraph_text_in_preview(self):
        return self.driver.find_element_by_id(self.PARAGRAPHS).text

    def check_download_link_is_present(self, document):
        return document.find_element_by_class_name(self.LINK_DOWNLOAD_CLASS).is_displayed()

    def get_document_text_in_edit_text_area(self):
        return self.driver.find_element_by_id(self.TEXT).text

    def select_and_return_first_checkbox_value(self):
        checkbox = self.driver.find_element_by_css_selector(self.PARAGRAPH_CHECKBOXES)
        checkbox.click()
        return checkbox.get_attribute("value")

    def add_text_to_edit_text(self, text):
        return self.driver.find_element_by_id(self.TEXT).send_keys(text)

    def click_regenerate_button(self):
        self.driver.find_element_by_id(self.LINK_REGENERATE_ID).click()

    def select_generate_document(self):
        self.driver.find_element_by_id(self.GENERATE_DECISION_DOCUMENT_BUTTON_ID).click()

    def select_document_template(self):
        self.driver.find_element_by_css_selector(self.DOCUMENT_TEMPLATE_CSS).click()

    def select_document_template_by_name(self, template_name):
        self.driver.find_element(by=By.XPATH, value=f"//img[@alt='{template_name}']").click()

    def get_item_from_siel_document_preview(self, item_name):
        headers = (
            td.text
            for td in self.driver.find_elements(by=By.XPATH, value="//div[@class = 'document']/table[2]/tbody/tr[4]/td")
        )
        values = (
            td.text
            for td in self.driver.find_elements(by=By.XPATH, value="//div[@class = 'document']/table[2]/tbody/tr[5]/td")
        )

        return dict(zip(headers, values))[item_name]

    def get_product_name_from_nlr_document_preview(self):
        return self.driver.find_element(
            by=By.XPATH, value="//div[@id='paragraph_content']/table/tbody/tr[1]/td[2]"
        ).text

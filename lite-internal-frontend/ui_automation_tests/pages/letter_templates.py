class LetterTemplates:

    def __init__(self, driver):
        self.driver = driver
        self.create_template_button = 'button-create-a-template'  # ID
        self.template_name = 'name'  # ID
        self.letter_paragraph = 'letter_paragraphs'  # NAME
        self.letter_paragraph_name = 'letter_paragraph_name'  # NAME
        self.add_letter_paragraph_button = '[value="add_letter_paragraph"]'  # CSS
        self.add_letter_paragraphs_button = '[value="return_to_preview"]'  # CSS
        self.preview_button = 'button-preview'  # ID
        self.preview_template_paragraphs = '.border-black.padding'  # CSS
        self.save_button = 'action'  # NAME
        self.edit_details_button = '.lite-app-bar__controls .govuk-button'  # CSS
        self.drag_drop_list = 'standard-advice-list'  # ID
        self.preview_paragraphs = 'paragraph-list'  # ID

        # Template page
        self.template_title = 'title'  # ID
        self.template_layout = 'layout'  # ID
        self.template_restricted_to = 'restricted_to'  # ID
        self.template_paragraphs = 'paragraph_content'  # ID
        self.edit_template_button = 'edit_template'  # ID
        self.edit_paragraphs_button = 'edit_template_paragraphs'  # ID
        self.add_paragraph_link = 'add_paragraph'  # ID
        self.paragraph_checkboxes_list = '.govuk-checkboxes__input'  # CSS
        self.paragraph_text_list = 'paragraph-list'  # ID

    def click_create_a_template(self):
        self.driver.find_element_by_id(self.create_template_button).click()

    def click_edit_details_button(self):
        self.driver.find_element_by_css_selector(self.edit_details_button).click()

    def click_create_preview_button(self):
        self.driver.find_element_by_id(self.preview_button).click()

    def enter_template_name(self, name):
        self.driver.find_element_by_id(self.template_name).clear()
        self.driver.find_element_by_id(self.template_name).send_keys(name)

    def select_which_type_of_case_template_can_apply_to(self, id_selector):
        self.driver.find_element_by_id(id_selector).click()

    def click_licence_layout(self, template_id):
        self.driver.find_element_by_id(template_id).click()

    def add_letter_paragraph(self):
        self.driver.find_element_by_name(self.letter_paragraph).click()
        return self.driver.find_element_by_name(self.letter_paragraph_name).text

    def click_save_button(self):
        self.driver.find_element_by_name(self.save_button).click()

    def click_add_letter_paragraph(self):
        self.driver.find_element_by_css_selector(self.add_letter_paragraph_button).click()

    def click_add_letter_paragraphs(self):
        self.driver.find_element_by_css_selector(self.add_letter_paragraphs_button).click()

    def get_text_of_paragraphs_in_template(self):
        return self.driver.find_element_by_css_selector(self.preview_template_paragraphs).text

    def get_text_of_paragraphs_in_preview(self):
        return self.driver.find_element_by_id(self.preview_paragraphs).text

    def get_class_name_of_drag_and_drop_list(self):
        return self.driver.find_element_by_id(self.drag_drop_list).get_attribute('class')

    def get_drag_and_drop_list_name(self):
        return self.driver.find_element_by_id(self.drag_drop_list).text

    def click_letter_template(self, document_template_name):
        self.driver.find_element_by_id(document_template_name).click()

    def get_template_title(self):
        return self.driver.find_element_by_id(self.template_title).text

    def get_template_layout(self):
        return self.driver.find_element_by_id(self.template_layout).text

    def get_template_restricted_to(self):
        return self.driver.find_element_by_id(self.template_restricted_to).text

    def get_template_paragraphs(self):
        return self.driver.find_element_by_id(self.template_paragraphs).text

    def click_edit_template_button(self):
        self.driver.find_element_by_id(self.edit_template_button).click()

    def click_edit_paragraphs_button(self):
        self.driver.find_element_by_id(self.edit_paragraphs_button).click()

    def click_add_paragraph_link(self):
        self.driver.find_element_by_id(self.add_paragraph_link).click()

    def get_add_paragraph_button(self):
        paragraph = self.driver.find_element_by_css_selector(self.paragraph_checkboxes_list)
        id = paragraph.get_attribute("value")
        paragraph.click()
        return id

    def get_list_of_letter_paragraphs(self):
        return self.driver.find_element_by_id(self.paragraph_text_list).text

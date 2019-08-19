from helpers.BasePage import BasePage


class GiveAdvicePages(BasePage):
    advice_checkbox_option = 'type-'  # ID
    import_advice_link = 'link-import-'  # ID
    picklist_item = 'app-picklist-picker__item'  # CSS
    picklist_item_text = '.app-picklist-picker__item p'  # CSS
    additional_notes = 'textarea-note'  # ID
    back_to_advice = 'Go back to the advice screen'  # link text

    def click_on_advice_option(self, option):
        self.driver.find_element_by_id(self.advice_checkbox_option + option).click()

    def click_on_import_advice_link(self, option):
        self.driver.find_element_by_id(self.import_advice_link + option).click()

    def click_on_picklist_item(self, option):
        self.driver.execute_script('document.getElementById("picklist-' + option + '").children[0].click()')
        self.driver.execute_script('document.getElementById("button-submit-' + option + '").click()')

    def get_text_of_picklist_item(self):
        return self.driver.find_element_by_css_selector(self.picklist_item_text).text

    def type_in_additional_note_text_field(self, text):
        return self.driver.find_element_by_id(self.additional_notes).send_keys(text)

    def click_go_back_to_advice_screen(self):
        self.driver.find_element_by_link_text(self.back_to_advice).click()
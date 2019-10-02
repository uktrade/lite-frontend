from helpers.BasePage import BasePage


class GiveAdvicePages(BasePage):
    advice_checkbox_option = 'type-'  # ID
    import_advice_link = 'link-import-'  # ID
    picklist_item = 'app-picklist-picker__item'  # CSS
    picklist_item_text = '.app-picklist-picker__item p'  # CSS
    additional_notes = 'textarea-note'  # ID
    back_to_advice = 'Go back to the advice screen'  # link text
    user_advice = 'user_advice'
    team_advice = 'team_advice'
    final_advice = 'final_advice'
    combine_advice_button = 'combine_advice_button'
    finalise_button = 'finalise_button'
    finalise_goods_and_countries_button = 'finalise_button'
    radio_input_approve = '.govuk-radios input[value="approve"]'

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

    def go_to_team_advice(self):
        self.driver.find_element_by_id(self.team_advice).click()

    def go_to_final_advice(self):
        self.driver.find_element_by_id(self.final_advice).click()

    def combine_advice(self):
        self.driver.find_element_by_id(self.combine_advice_button).click()

    def finalise(self):
        self.driver.find_element_by_id(self.finalise_button).click()

    def finalise_goods_and_countries(self):
        self.driver.find_element_by_id(self.finalise_goods_and_countries_button).click()

    def select_approve_for_all(self):
        elements = self.driver.find_elements_by_css_selector(self.radio_input_approve)
        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)

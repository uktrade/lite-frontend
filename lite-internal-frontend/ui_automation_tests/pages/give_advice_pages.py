from selenium.webdriver.support.select import Select

from shared.BasePage import BasePage


class GiveAdvicePages(BasePage):
    ADVICE_CHECKBOX_OPTION = "type-"  # ID
    IMPORT_ADVICE_LINK = "link-import-"  # ID
    PICKLIST_ITEM_TEXT = ".app-picklist-picker__item p"  # CSS
    DURATION_TEXT = "licence_duration"
    ADDITIONAL_NOTES = "textarea-note"  # ID
    TEAM_ADVICE = "team_advice"
    FINAL_ADVICE = "final_advice"
    COMBINE_ADVICE_BUTTON = "combine_advice_button"
    CLEAR_ADVICE_BUTTON = "button-clear-advice"
    FINALISE_BUTTON = "finalise_button"
    GIVE_OR_CHANGE_ADVICE_BUTTON = "button-give-advice"
    FINALISE_GOODS_AND_COUNTRIES_BUTTON = "finalise_button"
    CLEARANCE_LEVEL_DROPDOWN_ID = "pv_grading"
    RADIO_INPUT_APPROVE = '.govuk-radios input[value="approve"]'
    DAY = "day"
    MONTH = "month"
    YEAR = "year"

    def click_on_advice_option(self, option):
        self.driver.find_element_by_id(self.ADVICE_CHECKBOX_OPTION + option).click()

    def click_on_clear_advice(self):
        self.driver.find_element_by_id(self.CLEAR_ADVICE_BUTTON).click()

    def click_on_import_advice_link(self, option):
        self.driver.find_element_by_id(self.IMPORT_ADVICE_LINK + option).click()

    def click_on_picklist_item(self, option):
        self.driver.execute_script('document.getElementById("picklist-' + option + '").children[0].click()')
        self.driver.execute_script('document.getElementById("button-submit-' + option + '").click()')

    def get_text_of_picklist_item(self):
        return self.driver.find_element_by_css_selector(self.PICKLIST_ITEM_TEXT).text

    def type_in_additional_note_text_field(self, text):
        return self.driver.find_element_by_id(self.ADDITIONAL_NOTES).send_keys(text)

    def go_to_team_advice(self):
        self.driver.find_element_by_id(self.TEAM_ADVICE).click()

    def go_to_final_advice(self):
        self.driver.find_element_by_id(self.FINAL_ADVICE).click()

    def combine_advice(self):
        self.driver.find_element_by_id(self.COMBINE_ADVICE_BUTTON).click()

    def finalise(self):
        self.driver.find_element_by_id(self.FINALISE_BUTTON).click()

    def finalise_goods_and_countries(self):
        self.driver.find_element_by_id(self.FINALISE_GOODS_AND_COUNTRIES_BUTTON).click()

    def select_approve_for_all(self):
        elements = self.driver.find_elements_by_css_selector(self.RADIO_INPUT_APPROVE)
        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)

    def get_date_in_date_entry(self):
        return {
            "day": self.driver.find_element_by_id(self.DAY).get_attribute("value"),
            "month": self.driver.find_element_by_id(self.MONTH).get_attribute("value"),
            "year": self.driver.find_element_by_id(self.YEAR).get_attribute("value"),
        }

    def get_duration_in_finalise_view(self):
        return self.driver.find_element_by_id(self.DURATION_TEXT).get_attribute("value")

    def checkbox_present(self):
        return len(self.driver.find_elements_by_css_selector(".input"))

    def give_advice_button_present(self):
        return self.driver.find_elements_by_id(self.GIVE_OR_CHANGE_ADVICE_BUTTON)

    def clearance_grading_present(self):
        return self.driver.find_elements_by_id(self.CLEARANCE_LEVEL_DROPDOWN_ID)

    def select_clearance_grading(self, clearance_level):
        clearance_level_dropdown = Select(self.driver.find_element_by_id(self.CLEARANCE_LEVEL_DROPDOWN_ID))
        clearance_level_dropdown.select_by_visible_text(clearance_level)

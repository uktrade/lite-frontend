from ui_automation_tests.shared import functions
from ui_automation_tests.pages.BasePage import BasePage


class OgelPage(BasePage):
    CONTROL_LIST_ENTRY_ID = "control_list_entry"
    COUNTRY_ID = "country"
    FILTER_NAME_ID = "name"
    PARTIAL_OGEL_ID = "open_general_licence-"
    OGEL_TAB = "tab-open_general_licences"
    OGEL_ACCORDION_IN_RESULTS = "accordion-heading-1"

    def enter_control_list_entry(self, control_list_entry):
        functions.send_keys_to_autocomplete(self.driver, self.CONTROL_LIST_ENTRY_ID, control_list_entry)
        functions.click_submit(self.driver)

    def enter_country(self, country):
        functions.send_keys_to_autocomplete(self.driver, self.COUNTRY_ID, country)
        functions.click_submit(self.driver)

    def select_created_ogel(self, ogel_id):
        self.driver.find_element_by_id(self.PARTIAL_OGEL_ID + ogel_id).click()
        functions.click_submit(self.driver)

    def filter_by_name(self, name: str):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.FILTER_NAME_ID).clear()
        self.driver.find_element_by_id(self.FILTER_NAME_ID).send_keys(name)
        functions.apply_filters(self.driver)

    def click_ogel_tab(self):
        self.driver.find_element_by_id(self.OGEL_TAB).click()

    def get_text_of_ogel_accordion(self):
        return self.driver.find_element_by_id(self.OGEL_ACCORDION_IN_RESULTS).text

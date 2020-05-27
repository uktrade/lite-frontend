from ui_automation_tests.shared import functions
from ui_automation_tests.pages.BasePage import BasePage


class OpenApplicationAddGoodsType(BasePage):

    INPUT_DESCRIPTION_ID = "description"
    TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR = "#pane_control_list_entries .tokenfield-input"
    RADIO_IS_GOOD_CONTROLLED_ID = "is_good_controlled-"
    RADIO_IS_GOOD_INCORPORATED_ID = "is_good_incorporated-"

    def enter_description(self, value):
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_ID).send_keys(value)

    def select_is_your_good_controlled(self, value):
        self.driver.find_element_by_id(self.RADIO_IS_GOOD_CONTROLLED_ID + value.lower()).click()

    def enter_control_list_entry(self, control_list_entry):
        functions.send_tokens_to_token_bar(
            self.driver, self.TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR, [control_list_entry]
        )

    def select_is_your_good_incorporated(self, value):
        self.driver.find_element_by_id(self.RADIO_IS_GOOD_INCORPORATED_ID + str(value.lower() == "yes")).click()

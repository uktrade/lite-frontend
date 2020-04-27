from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class GoodsListPage(BasePage):

    BUTTON_ADD_A_GOOD_ID = "button-add-a-good"
    INPUT_DESCRIPTION_FILTER_ID = "description"
    INPUT_CONTROL_LIST_ENTRY_FILTER_ID = "control_list_entry"
    INPUT_PART_NUMBER_FILTER_ID = "part_number"
    BUTTON_APPLY_FILTERS = "button-apply-filters"

    def get_good_row(self, index: int):
        """
        Returns the goods table row at the index given.
        Args:
            index: Index of good in table, starts at 0
        """
        return self.driver.find_elements_by_css_selector(f"{Shared.GOV_TABLE_ROW}:nth-of-type({index + 1})")

    def click_view_good(self, index: int):
        """
        Clicks the view link on a table row at the index given.
        Args:
            index: Index of good in table, starts at 0
        """
        self.driver.find_elements_by_css_selector(f"{Shared.GOV_TABLE_ROW}:nth-of-type({index + 1}) a")[-1].click()

    def click_add_a_good(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_GOOD_ID).click()

    def filter_by_description(self, description: str):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_FILTER_ID).clear()
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_FILTER_ID).send_keys(description)
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTERS).click()

    def filter_by_control_list_entry(self, control_list_entry: str):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_CONTROL_LIST_ENTRY_FILTER_ID).clear()
        self.driver.find_element_by_id(self.INPUT_CONTROL_LIST_ENTRY_FILTER_ID).send_keys(control_list_entry)
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTERS).click()

    def filter_by_part_number(self, part_number: str):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_PART_NUMBER_FILTER_ID).clear()
        self.driver.find_element_by_id(self.INPUT_PART_NUMBER_FILTER_ID).send_keys(part_number)
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTERS).click()
